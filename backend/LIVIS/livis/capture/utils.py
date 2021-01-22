import os
from kafka import KafkaProducer,  KafkaConsumer
import json
import cv2
import numpy as np
import base64
import time
import sys
import logging
import pandas as pd
from pymongo import MongoClient
from common.utils import MongoHelper
from bson import ObjectId
import multiprocessing
from .consumer import *
from livis.settings import *

KAFKA_BROKER_URL = "127.0.0.1:9092"
consumer_mount_path = "/apps/Livis"
#consumer_mount_path = IMAGE_DATASET_SAVE_PATH




def get_camera_feed_urls():

    try:
        mp = MongoHelper().getCollection(WORKSTATION_COLLECTION)
    except:
        message = "Cannot connect to db"
        status_code = 500
        return message,status_code


    p = [p for p in mp.find()]

    p=p[0]

    workstation_id = p['_id']

    feed_urls = []
    dummmy_dct = {}
    
    
    workstation_id = ObjectId(workstation_id)
    mp = MongoHelper().getCollection(WORKSTATION_COLLECTION)
    ws_row = mp.find_one({'_id': workstation_id})
    ws_camera_dict = ws_row.get('cameras')
    print(ws_camera_dict)
    
    for i in ws_camera_dict:
        
        url = "http://127.0.0.1:8000/livis/v1/capture/consumer_camera_preview/{}/{}/".format(workstation_id,i['camera_name'])
        dummmy_dct = {"camera_name":i['camera_name'] , "camera_url":url}
        feed_urls.append(dummmy_dct)
    if feed_urls:
        return feed_urls
    else:
        return {}
    
    

        

def start_consumer_video_stream(data):

    logging.basicConfig(filename='Status_consumer.log',
                        level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

    try:
        part_id = data['part_id']
    except:
        message = "part id not provided"
        status_code = 400
        return message, status_code
        
    try:
        workstation_id = data['workstation_id']
    except:
        message = "workstation id not provided"
        status_code = 400
        return message, status_code

    try:
        camera_id = data['camera_id']
    except:
        message = "camera id not provided"
        status_code = 400
        return message, status_code

    # # access the workstation table
    # workstation_id = ObjectId(workstation_id)
    # mp = MongoHelper().getCollection(WORKSTATION_COLLECTION)
    # ws_row = mp.find_one({'_id': workstation_id})
    # ws_camera_dict = ws_row.get('cameras')
    #
    # for key, value in ws_camera_dict.iter():
    #     if key == camera_name:
    #         camera_id = ws_camera_dict[key]

    camera_name = "0"
    camera_id = camera_name

    logging.info('Creating the Consumer object for streaming')

    topic = str(part_id) + str(workstation_id) + str(camera_id)
    # Creating a folder to store the images consumed, folder name is part name
    img_database_path = consumer_mount_path + "/" + str(part_id)
    if os.path.exists(img_database_path):
        pass
    else:
        os.makedirs(img_database_path)


    try:
        consumer = Consumer(KAFKA_BROKER_URL, topic, auto_offset_reset_value='earliest')
    except:
        message = "Consumer object creation failed"
        status_code = 415
        return message, status_code

    # Streaming the frames
    logging.info('Initiating the consumer')

    consumer.collect_stream_for_capture(part_id, workstation_id)
    logging.info('Done receiving streaming')
    message = "Done receiving streaming"
    status_code = 200
    return message, status_code


def start_consumer_camera_preview(workstation_id,camera_name):


    # access the workstation table
    workstation_id = ObjectId(workstation_id)
    mp = MongoHelper().getCollection(WORKSTATION_COLLECTION)
    ws_row = mp.find_one({'_id': workstation_id})
    ws_camera_dict = ws_row.get('cameras')
    print(ws_camera_dict)
    #list_of_cam = []
    
    #for i in ws_camera_dict:
    #   camera_id = i['camera_id']
    #    list_of_cam.append(camera_id)
    
    for i in ws_camera_dict:
        camera_id = i['camera_id']
        camera_name1 = i['camera_name']
        if camera_name1 ==  camera_name:
            break
    
    
    topic = str(workstation_id) + "_" + str(camera_id)
    print(topic)

    #try:
    #    consumer = Consumer(KAFKA_BROKER_URL, topic, auto_offset_reset_value='earliest')
    #except Exception as e:
    #    print(e)
    #    message = "Consumer object creation failed"
    #    status_code = 415
    #    return message, status_code

    # Streaming the frames
    logging.info('Initiating the consumer')
    
    consumer = KafkaConsumer(topic, bootstrap_servers=KAFKA_BROKER_URL, auto_offset_reset='latest')
        #value_deserializer=lambda value: json.loads(value), auto_offset_reset='earliest',)
        
    for message in consumer:
        #print("called2")
        #print(message.value.decode('utf-8'))
        a = message.value.decode('utf-8')
        b = json.loads(a)
        #print(type(b))
        #break
        
        im_b64_str = b["frame"]
        im_b64 = bytes(im_b64_str[2:], 'utf-8')
        im_binary = base64.b64decode(im_b64)

        im_arr = np.frombuffer(im_binary, dtype=np.uint8)
        img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
            

        ret, jpeg = cv2.imencode('.jpg', img)
        #print(jpeg)
        cv2.imwrite("frane.jpg",jpeg)
        
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    
    

    #return consumer.collect_stream_for_preview("", workstation_id)
    
    #logging.info('Done receiving streaming')
    #message = "Done receiving streaming"
    #status_code = 200
    #return message, status_code




