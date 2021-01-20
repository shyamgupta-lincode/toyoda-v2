import os
from kafka import KafkaProducer
import json
import cv2
import numpy as np
import base64
import time
import sys
import logging
import shutil
#from .utils import MongoHelper
import multiprocessing
from .producer import *
from bson import ObjectId

KAFKA_BROKER_URL = "broker:9092"


def start_producer_bulk_upload_stream(data):
    #Creating a logging object
    logging.basicConfig(filename='Status_producer.log',
                         level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    try:
        compressed_file_path = data['compressed_file_path']
    except:
        message = "File path not found"
        status_code = 400
        return message, status_code

    try:
        compression_format = data['compression_format']
    except:
        message = "Compression format not provided"
        status_code = 400
        return message, status_code

    try:
        part_id = data['part_id']
    except:
        message = "part id not provided"
        status_code = 400
        return message, status_code

    try:
        workstation_id = data['workstation_id']
    except:
        message = "Workstation ID not provided"
        status_code = 400
        return message, status_code

    logging.info('Creating the Producer object for streaming')

    topic = str(part_id) + str(workstation_id)

    try:
        producer_ws = Producer(KAFKA_BROKER_URL, topic)
    except:
        message = "Producer object creation failed"
        status_code = 415
        return message, status_code

    logging.info('Initiating the stream')
    producer_ws.stream_bulk_upload_data(compressed_file_path, compression_format, part_id, workstation_id)
    logging.info('Done streaming')
    message = "Done streaming"
    status_code = 200
    return message, status_code


def start_producer_video_stream(data):

    logging.basicConfig(filename='Status_producer.log',
                        level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

    try:
        workstation_id = data['wid']
    except:
        message = "workstation id not provided"
        status_code = 400
        return message, status_code

    try:
        part_id = data['partid']
    except:
        message = "part id not provided"
        status_code = 400
        return message, status_code

    try:
        camera_name = data['cameraname']
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

    topic = str(workstation_id)+str(part_id)+str(camera_id)

    logging.info('Creating the Producer object for streaming')
    try:
        producer_ws = Producer(KAFKA_BROKER_URL, topic)
    except:
        message = "Producer object creation failed"
        status_code = 415
        return message, status_code

    ## Streaming the frames
    logging.info('Initiating the stream')
    status_code = producer_ws.stream_video(part_id, workstation_id, camera_id)
    logging.info('Done streaming')
    print("status code after streaming " + str(status_code))
    message = "Done streaming"
    return message, status_code


def start_camera_selection(data):
    # get data from the JSON POST object
    logging.basicConfig(filename='Status_producer.log',
                        level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

    try:
        part_id_json = data['part_id']
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
        camera_select_list_from_post = data['camera_selected']
    except:
        message = "camera selected list not provided"
        status_code = 400
        return message, status_code

    try:
        overwrite_flag = data['overwrite_flag']
    except:
        overwrite_flag = False


    # access the parts table
    part_id = ObjectId(part_id_json)
    mp = MongoHelper().getCollection(PARTS_COLLECTION)
    part_row = mp.find_one({'_id': part_id})
    parts_camera_dict = part_row.get('camera_selected')

    ## Logic for if camera_selected not exist
    if parts_camera_dict == {}:#--- Check this condition
        parts_camera_dict[workstation_id] = camera_select_list_from_post
        part_row['camera_selected'] = parts_camera_dict
        mp.update({'_id': part_row['_id']}, {'$set': part_row})
        message = "Camera selected list updated successfully"
        status_code = 200
        return message, status_code
    else:
        ## Logic for if camera_selected exists
        if overwrite_flag == True:
            for key in parts_camera_dict:
                if key == workstation_id:
                    parts_camera_dict[key] = camera_select_list_from_post
                    part_row['camera_selected'] = parts_camera_dict
                    mp.update({'_id': part_row['_id']}, {'$set': part_row})
                    message = "Camera selection updated"
                    status_code = 200
                    return message, status_code

        else:
            for key in parts_camera_dict:
                if key == workstation_id:
                    ### Checking for overwrite camera id's [camera_id's present and need to be raised]
                    existing_camera_list = parts_camera_dict[key]
                    for current_ in existing_camera_list:
                        if current_ in camera_select_list_from_post:
                            experiments_list = MongoHelper().getCollection(part_id+"_experiment")
                            p = [p for p in experiments_list.find()]
                            for experiment in p:
                                experiment_status = experiment.get('status')
                                if experiment_status == "Running":
                                    message = "Overwrite flag is raised"
                                    status_code = 422
                                    return message, status_code
                    for new_ in camera_select_list_from_post:
                        if new_ not in existing_camera_list:
                            existing_camera_list.append(new_)
                    parts_camera_dict[key] = existing_camera_list
                    part_row['camera_selected'] = parts_camera_dict
                    mp.update({'_id': part_row['_id']}, {'$set': part_row})
                    message = "Camera selection updated"
                    status_code = 200
                    return message, status_code


def start_camera_preview(data):

    try:
        workstation_id = data['wid']
    except:
        message = "workstation id not provided"
        status_code = 400
        return message, status_code

    try:
        camera_name = data['cameraname']
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

    topic = str(workstation_id)+str(camera_id)

    logging.info('Creating the Producer object for streaming')
    try:
        producer_ws = Producer(KAFKA_BROKER_URL, topic)
    except:
        message = "Producer object creation failed"
        status_code = 415
        return message, status_code

    ## Streaming the frames
    logging.info('Initiating the stream')
    status_code = producer_ws.stream_video("", workstation_id, camera_id)
    logging.info('Done streaming')
    print("status code after streaming " + str(status_code))
    message = "Done streaming"
    return message, status_code









