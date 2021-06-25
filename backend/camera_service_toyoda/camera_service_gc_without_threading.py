import cv2
import redis
import json
from common_utils import *
from setting_keys import *
import threading
import datetime
import gc
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
from kafka_utils import imEncoder
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


KAFKA_BROKER_URL="localhost:9092"

def camera_initialize(camera_index):
    # video = cv2.VideoCapture(int(camera_index), cv2.CAP_DSHOW)

    # video_file = '/home/toyoda/livis_v2_toyota/republic/backend/camera_service3 _auto/4.mp4'
    
    # video = cv2.VideoCapture(int(camera_index))
    video = cv2.VideoCapture(camera_index)
    
    print('publishing video...')

    # while(video.isOpened()):
    #     success, frame_ = video.read()

    #     # Ensure file was read successfully
    #     if not success:
    #         print("bad read!")
    #         break
        

    #cap = cv2.VideoCapture(camera_index)
    #cap.set(cv2.CAP_PROP_AUTOFOCUS,0)
    # cap.set(cv2.CAP_PROP_FOCUS,int(40))


    video.set(cv2.CAP_PROP_FRAME_HEIGHT,720)
    video.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
    return video



cam_t0 = datetime.datetime.now() 
# wid = json.load(open("workstation_id.json"))
wid = json.load(open(WORKSTATION_ID_PATH))
data = RedisKeyBuilderServer(wid).workstation_info
print("data..............>>>", data)



# data_kafka = KafkaBuilderServer(wid).workstation_info

# print("data_kafka ....",data_kafka)
#Calling redis module
rch = CacheHelper()

cam_list = []
key_list = []
cap_list = []


for cam in data['cameras']:
    try:
        camera_index = int(cam['camera_id'])
    except:
        camera_index = cam['camera_id']

    camera_name = cam['camera_name']
    #print("camera_name........",camera_name)
    key = RedisKeyBuilderServer(wid).get_key(cam['camera_id'],original_frame_keyholder) #WS-01_0_original-frame
    # key_kafka  = KafkaBuilderServer(wid).get_key(cam['camera_id'],original_frame_keyholder)
    # cap = camera_initialize(camera_index = int(camera_index))
    cap = camera_initialize(camera_index = camera_index)
    cap_list.append(cap)
    cam_list.append(cam['camera_name'])
    key_list.append(key)

cam_t1 = datetime.datetime.now()
print("key list...........", key_list)
print("cap list..........", cap_list)
print("cam_list ...........",cam_list)

#################################Kafka############### 

#######################################################

producer =  KafkaProducer(bootstrap_servers=['localhost:9092'])

gc_counter = 0
while True:
    # try:
    for cap, key, cam_name in zip(cap_list, key_list,cam_list):
        st = time.time()
        ret, frame = cap.read()
        
        # rch.set_json({key:frame})
        # ret, buffer = cv2.imencode('.jpg', frame)
        # image_dict = {"frame":buffer.tobytes()
        kafka_key = key+"_"+cam_name
        print(cam_name)
        image_buffer = imEncoder(frame)
        payload = {"frame":image_buffer}
        print("Kafka topic:",kafka_key)
        serialized_data = json.dumps(payload).encode('utf-8')
        print(type(serialized_data))
        producer.send(kafka_key, serialized_data)

        end = time.time() -st

        print(end)
        # print(key,frame)
        print("Kafka:",kafka_key)
        if "top" in kafka_key.split('_'):

            cv2.imwrite("camera_Service_image.jpg", cv2.resize(frame,(640, 480)))
        # cv2.imshow("frame",frame)
        del frame
        del key
        if gc_counter % 1000 == 0:
            collected = gc.collect()
            print("GC Collected>>>>>>>>", collected)
        gc_counter+=1
        # print(gc_counter)

    # except Exception as e:
    #     print("Exception Encountered")
    #     print(str(e))
    #     pass

    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
  
cv2.destroyAllWindows() 
