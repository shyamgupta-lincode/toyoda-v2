import urllib
import cv2
import numpy as np
import urllib.request
import matplotlib.pyplot as plt
import os
import time
import tensorflow as tf
import sys
import datetime
import base64
from kafka import KafkaProducer
import json
import logging
import pymongo
#from common.utils import MongoHelper
#from livis.settings import *
from kafka import KafkaProducer
import multiprocessing
import threading
from PIL import Image, ImageEnhance
from matplotlib import cm
import numpy
from pymongo import MongoClient

KAFKA_BROKER_URL="13.127.161.4:9092"
MONGO_SERVER_HOST="13.234.202.181"
MONGO_SERVER_PORT=7778
MONGO_DB = "LIVIS"
WORKSTATION_COLLECTION='workstations'
MONGO_COLLECTION_PARTS = "parts"
MONGO_COLLECTIONS = {MONGO_COLLECTION_PARTS: "parts"}

def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance


@singleton
class MongoHelper:
    client = None
    def __init__(self):
        if not self.client:
            self.client = MongoClient(host=MONGO_SERVER_HOST, port=MONGO_SERVER_PORT)
        self.db = self.client[MONGO_DB]

    def getDatabase(self):
        return self.db

    def getCollection(self, cname, create=False, codec_options=None):
        _DB = MONGO_DB
        DB = self.client[_DB]
        if cname in MONGO_COLLECTIONS:
            if codec_options:
                return DB.get_collection(MONGO_COLLECTIONS[cname], codec_options=codec_options)
            return DB[MONGO_COLLECTIONS[cname]]
        else:
            return DB[cname]


class IPWEBCAM(object):
    def __init__(self, root_url='10.60.60.254:8080', width=400, height=400):
        self.url = 'http://'+root_url
        self.width = width
        self.height = height
        self.resolutions = {
                "0" : "1920x1080",
                "1" : "1280x720",
                "2" : "960x720",
                "3" : "720x480",
                "4" : "640x480",
                "5" : "352x288",
                "6" : "320x240",
                "7" : "256x144",
                "8" : "176x144"
                }

    def get_image(self):
        # Get our image from the phone
        imgResp = urllib.request.urlopen(self.url + '/shot.jpg')
        # Convert our image to a numpy array so that we can work with it
        imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
        # Convert our image again but this time to opencv format
        img = cv2.imdecode(imgNp,-1)
        return img

class Camera():
    def __init__(self, KAFKA_BROKER_URL, topic, camera_id):
        self.tfms = {}
        self.KAFKA_BROKER_URL = KAFKA_BROKER_URL
        self.topic = topic
        self.cam_id = camera_id
        #self.cap = IPWEBCAM(root_url="10.60.60.254:8080")
        self.frame = None
        self.part_id = None
        self.killed = False
        self.thread = None
        self.producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER_URL,
                             value_serializer=lambda value: json.dumps(value).encode(), )
        self.th = None
        self.poll_for_part_id()


        if str(camera_id).find(".") == -1:
            self.cap = cv2.VideoCapture(int(self.cam_id))
            self.is_ip = False
        else:
            self.cap = IPWEBCAM(root_url=str(self.cam_id))
            self.is_ip = True
            print("mobile found")


    def _poll_for_part_id(self):
        mp = MongoHelper().getCollection("cam_to_part")
        while True:
            #pr = mp.find_one({'camera_id' : int(self.cam_id)})
            if self.cam_id.find(":") != -1:
                pr = mp.find_one({'camera_id' : self.cam_id})
            else:
                pr = mp.find_one({'camera_id' : int(self.cam_id)})
            if pr:
                #print('found_part : : : ' , pr)
                self.part_id = pr['part_id']

    def poll_for_part_id(self):
        self.th = threading.Thread(target=self._poll_for_part_id)
        self.th.start()

    def _start(self):
        while not self.killed:
            #print(self.is_ip)
            if self.is_ip == False:
                try:
                    ret, self.frame = self.cap.read()
                except:
                    continue
            if self.is_ip == True:
                try:
                    self.frame = self.cap.get_image()
                except:
                    continue
            if self.frame is None:
                #print("None Frame Recieved!")
                continue
            #### check tfms and apply here
            if self.part_id:
                self.tfms = self.get_tfms()
                if self.tfms:
                    print(self.tfms)
                    self.apply_transform()
            ####
            self.publish_frame_to_kafka()

    def publish_frame_to_kafka(self):
        f_name = str(self.cam_id) + "_tmp.jpg"
        cv2.imwrite(f_name, self.frame)
        with open(f_name, 'rb') as f:
            im_b64 = base64.b64encode(f.read())
        payload_video_frame = {"frame": str(im_b64)}
        future = self.producer.send(self.topic, value=payload_video_frame)
        report = future.get()

    def get_tfms(self):
        self.tfms = {}
        if self.part_id:
            mp = MongoHelper().getCollection(self.part_id + "_preprocessingpolicy")
            pre = mp.find_one({'camera_id' : str(self.cam_id)})
            p = pre['policy']
            for key, value in p.items():
                if key in ['brightness', 'contrast', 'hue', 'saturation']:
                    self.tfms[key] = value
                    #print(self.tfms[key])
        return self.tfms

    def apply_transform(self):
        if self.tfms:
            for k,val in self.tfms.items():
                val = float(val)
                print('applying tfms {}'.format(k))
                if k == 'brightness':
                    if val != 0:
                        val = val * 100
                        hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
                        h, s, v = cv2.split(hsv)
                        v = cv2.add(v,val)
                        v[v > 255] = 255
                        v[v < 0] = 0
                        final_hsv = cv2.merge((h, s, v))
                        self.frame = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
                    else:
                        self.frame = self.frame
                if k == 'contrast':
                    if val != 0:
                        val = val * 3
                        print("val is:",val)
                        ff = Image.fromarray(np.uint8(self.frame)).convert('RGB')
                        f=ImageEnhance.Contrast(ff)
                        e_img=f.enhance(val)
                        self.frame = numpy.asarray(e_img)
                    else:
                        self.frame = self.frame

    def start(self):
        self.thread = threading.Thread(target=self._start)
        self.thread.start()

    def stop(self):
        self.killed = True
        time.sleep(0.2)
        self.thread.join()
        self.thread = None
        self.killed = False
