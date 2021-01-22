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

class Producer():
    """
        Publishes video data from camera to topic
    """
    def __init__(self, KAFKA_BROKER_URL, topic):
        """
        Instantiates the Producer object

        Arguments:
            KAFKA_BROKER_URL: url to connect to Broker
            part: part id/name that is being captured
            topic: topic to publish video stream to
        """
        print(KAFKA_BROKER_URL)
        self.obj = KafkaProducer(bootstrap_servers=KAFKA_BROKER_URL)
                             #value_serializer=lambda value: json.dumps(value), )
        self.topic = topic


    def stream_video(self, camera_index,producer,topic):
        """
        Accesses frames from the camera, encodes it and publishes it to the respective topic

        Arguments:
            file_format: format of the image data to be sent to the Kafka consumer
        """
        #camera = neoapi.Cam()
        #print(camera.Connect(camera_index))
        cap = cv2.VideoCapture(int(camera_index))
        
        #time.sleep(2)
        width = 1280
        height = 720
        start = datetime.datetime.now()
        
        
        return 0



### Access the mongo collection for wid cameraname

wid = "60070cc41ad3c5ef42aeca72"
camera_id = "0"

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

print(list_of_topics)



"""
#### Create kafka topic wid_camera_id
topic = str(wid) + "_" + str(camera_id)
#print(topic)
KAFKA_BROKER_URL = "127.0.0.1:9092"
producer_ws = Producer(KAFKA_BROKER_URL, topic)

logging.info('Initiating the stream')
#status_code = producer_ws.stream_video(camera_id)
"""

def start_multiprocess_stream(KAFKA_BROKER_URL, topic,camera_id):
    
    producer = KafkaProducer(bootstrap_servers='127.0.0.1:9092',value_serializer=lambda value: json.dumps(value).encode(),)
    
    cap = cv2.VideoCapture(int(camera_id))
    print(topic)
    while True:
        ret,img = cap.read()
        if img is None:
            print("none frame recieved")
            continue
        f_name  = str(camera_id) + "_tmp.jpg"
        cv2.imwrite(f_name, img)
        with open(f_name,'rb') as f:
    	    im_b64 = base64.b64encode(f.read())
        payload_video_frame = {"frame": str(im_b64)}
        producer.send(topic, value=payload_video_frame)
    
    return 0

jobs = []
list_of_process = []
for i in list_of_topics:

  
    
    topic = i
    camera_id = int( topic.split('_')[1] ) 
    
    p = multiprocessing.Process(target=start_multiprocess_stream, args=(KAFKA_BROKER_URL, topic,camera_id,))
    p.start()

p.join()
    



            




"""
    #status_code = producer_ws.stream_video(camera_id,producer,topic)





    #img = camera.GetImage().GetNPArray()
    
    #if len(img) == 0:
    #   time.sleep(0.2)
    #    continue
    
        
    #    continue
    #img = cv2.resize(img, (width, height))
    #stop = datetime.datetime.now()
    #print(stop - start)
    title = 'Press [ESC] to exit ..'
    #start = datetime.datetime.now()
    
    #im_b64 = base64.b64encode(img)
    
    
    #print(self.topic)
    #print(payload_video_frame)
    #self.obj.send(self.topic, value=payload_video_frame)
    print(topic)
    
            
    #time.sleep(1)
"""




