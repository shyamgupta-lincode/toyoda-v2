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

KAFKA_BROKER_URL = "broker:9092"
#consumer_mount_path = "/apps/Livis"
consumer_mount_path = IMAGE_DATASET_SAVE_PATH


def start_consumer_video_stream(data):

    logging.basicConfig(filename='Status_consumer.log',
                        level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

    try:
        part_id = data['partid']
    except:
        message = "part id not provided"
        status_code = 400
        return message, status_code
        
    try:
        workstation_id = data['wid']
    except:
        message = "workstation id not provided"
        status_code = 400
        return message, status_code

    try:
        camera_name = data['camera_name']
    except:
        message = "camera name not provided"
        status_code = 400
        return message, status_code

    # access the workstation table
    workstation_id = ObjectId(workstation_id)
    mp = MongoHelper().getCollection(WORKSTATION_COLLECTION)
    ws_row = mp.find_one({'_id': workstation_id})
    ws_camera_dict = ws_row.get('cameras')

    for key, value in ws_camera_dict.iter():
        if key == camera_name:
            camera_id = ws_camera_dict[key]

    logging.info('Creating the Consumer object for streaming')

    topic = str(part_id) + str(workstation_id) + str(camera_id)
    # Creating a folder to store the images consumed, folder name is part name
    img_database_path = consumer_mount_path + "/" + str(part_id)
    if os.path.exists(img_database_path):
        pass
    else:
        os.makedirs(img_database_path)


    try:
        consumer = Consumer(KAFKA_BROKER_URL, topic, auto_offset_reset_value='latest', consumer_timeout_ms=30000)
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


def start_consumer_camera_preview(data):
    try:
        workstation_id = data['workstation_id']
    except:
        message = "workstation id not provided"
        status_code = 400
        return message, status_code

    try:
        camera_name = data['camera_name']
    except:
        message = "camera name not provided"
        status_code = 400
        return message, status_code

    # access the workstation table
    workstation_id = ObjectId(workstation_id)
    mp = MongoHelper().getCollection(WORKSTATION_COLLECTION)
    ws_row = mp.find_one({'_id': workstation_id})
    ws_camera_dict = ws_row.get('cameras')

    for key, value in ws_camera_dict.iter():
        if key == camera_name:
            camera_id = ws_camera_dict[key]

    topic = str(workstation_id) + str(camera_id)

    try:
        consumer = Consumer(KAFKA_BROKER_URL, topic, auto_offset_reset_value='latest', consumer_timeout_ms=30000)
    except:
        message = "Consumer object creation failed"
        status_code = 415
        return message, status_code

    # Streaming the frames
    logging.info('Initiating the consumer')

    consumer.collect_stream_for_preview("", workstation_id)
    logging.info('Done receiving streaming')
    message = "Done receiving streaming"
    status_code = 200
    return message, status_code




