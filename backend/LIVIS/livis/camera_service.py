import sys
import cv2
#import neoapi
import time
import datetime
import os
import time
import base64
import cv2
from kafka import KafkaProducer
import json
import logging
import pymongo
import sys
from common.utils import MongoHelper
from livis.settings import *
from kafka import KafkaProducer
import multiprocessing
import threading
from PIL import Image, ImageEnhance
from matplotlib import cm
import numpy as np
import numpy

class Camera():
    def __init__(self, KAFKA_BROKER_URL, topic, camera_id):
        self.tfms = {}
        self.KAFKA_BROKER_URL =  KAFKA_BROKER_URL
        self.topic = topic
        self.cam_id = camera_id
        self.cap = cv2.VideoCapture(int(self.cam_id))
        self.frame = None
        self.part_id = None
        self.killed = False
        self.thread = None
        self.producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER_URL,
                             value_serializer=lambda value: json.dumps(value).encode(), )
        self.th = None
        self.poll_for_part_id()
    def _poll_for_part_id(self):
        mp = MongoHelper().getCollection("cam_to_part")
        while True:
            pr = mp.find_one({'camera_id' : int(self.cam_id)})
            if pr:
                #print('found_part : : : ' , pr)
                self.part_id = pr['part_id']
    def poll_for_part_id(self):
        self.th = threading.Thread(target=self._poll_for_part_id)
        self.th.start()
    def _start(self):
        while not self.killed:
            ret, self.frame = self.cap.read()
            if self.frame is None:
                print("None Frame Recieved!") 
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



"""
def start_multiprocess_stream(KAFKA_BROKER_URL, topic, camera_id):
    producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER_URL,
                             value_serializer=lambda value: json.dumps(value).encode(), )

    cap = cv2.VideoCapture(int(camera_id))
    print(camera_id)

    while True:
        ret, img = cap.read()
        if img is None:
            print("none frame recieved")
            
            #print(camera_id)
            continue
        f_name = str(camera_id) + "_tmp.jpg"
        cv2.imwrite(f_name, img)
        with open(f_name, 'rb') as f:
            im_b64 = base64.b64encode(f.read())
        payload_video_frame = {"frame": str(im_b64)}
        future = producer.send(topic, value=payload_video_frame)
        report = future.get()
        
        print(report.offset)

    return 0

"""


list_of_topics = []
mp = MongoHelper().getCollection(WORKSTATION_COLLECTION)
workstations = [p for p in mp.find({"$and" : [{"isdeleted": False}, { "isdeleted" : {"$exists" : True}}]})]
print(len(workstations))


if workstations:
    for w_s in workstations:
        cameras = w_s['cameras']
        wids = w_s['_id']
        for c in cameras:
            camera_ids = c['camera_id']
            list_of_topics.append(str(wids)+"_"+str(camera_ids)+"_input")




for i in list_of_topics:
    topic = i
    camera_id = int(topic.split('_')[1])

    #p = multiprocessing.Process(target=start_multiprocess_stream, args=(KAFKA_BROKER_URL, topic,camera_id,))
    #p.start()

    cc = Camera(KAFKA_BROKER_URL, topic, camera_id)
    cc.start()



#p.join()
