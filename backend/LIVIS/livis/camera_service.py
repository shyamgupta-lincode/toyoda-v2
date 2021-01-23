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


def start_multiprocess_stream(KAFKA_BROKER_URL, topic, camera_id):
    producer = KafkaProducer(bootstrap_servers='127.0.0.1:9092',
                             value_serializer=lambda value: json.dumps(value).encode(), )

    cap = cv2.VideoCapture(int(camera_id))
    print(topic)
    while True:
        ret, img = cap.read()
        if img is None:
            print("none frame recieved")
            continue
        f_name = str(camera_id) + "_tmp.jpg"
        cv2.imwrite(f_name, img)
        with open(f_name, 'rb') as f:
            im_b64 = base64.b64encode(f.read())
        payload_video_frame = {"frame": str(im_b64)}
        producer.send(topic, value=payload_video_frame)

    return 0


w_c_dct = []
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
            list_of_topics.append(str(wids)+"_"+str(camera_ids))


jobs = []
list_of_process = []
for i in list_of_topics:
    topic = i
    camera_id = int(topic.split('_')[1])
    
    p = multiprocessing.Process(target=start_multiprocess_stream, args=(KAFKA_BROKER_URL, topic,camera_id,))
    p.start()

p.join()



