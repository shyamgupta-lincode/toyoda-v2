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
    
    
    workstation_id = ObjectId(workstation_id)
    mp = MongoHelper().getCollection(WORKSTATION_COLLECTION)
    ws_row = mp.find_one({'_id': workstation_id})
    ws_camera_dict = ws_row.get('cameras')
    print(ws_camera_dict)
    
    for i in ws_camera_dict:
        url = "http://127.0.0.1:8000/livis/v1/capture/consumer_camera_preview/{}/{}/".format(workstation_id,i['camera_name'])
        feed_urls.append(url)
    if feed_urls:
        return feed_urls
    else:
        return {}


def apply_crops(img, x,y,w,h):
    height,width,channels = img.shape
    x0 = x * width
    y0 = y * height
    x1 = ((x + w) * width)
    y1 = ((y + h) * height)
    img = img[y0:y1,x0:x1]
    return img
    
    
def start_video_stream(workstation_id, part_id, camera_name):
    # access the workstation table
    workstation_id = ObjectId(workstation_id)
    mp = MongoHelper().getCollection(WORKSTATION_COLLECTION)
    ws_row = mp.find_one({'_id': workstation_id})
    ws_camera_dict = ws_row.get('cameras')

    for i in ws_camera_dict:
        camera_id = i['camera_id']
        camera_name1 = i['camera_name']
        if camera_name1 == camera_name:
            break

    topic = str(workstation_id) + "_" + str(camera_id)

    consumer = KafkaConsumer(topic, bootstrap_servers=KAFKA_BROKER_URL, auto_offset_reset='latest')

    for message in consumer:
        a = message.value.decode('utf-8')
        b = json.loads(a)

        im_b64_str = b["frame"]
        im_b64 = bytes(im_b64_str[2:], 'utf-8')
        im_binary = base64.b64decode(im_b64)

        im_arr = np.frombuffer(im_binary, dtype=np.uint8)
        img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)

        ret, jpeg = cv2.imencode('.jpg', img)
        cv2.imwrite("frame.jpg", jpeg)
        preprocessing_list = MongoHelper().getCollection(part_id + "_preprocessingpolicy")
        p = [p for p in preprocessing_list.find()]
        iter_ = 0
        for policy in p:
            if policy['workstation_id'] == workstation_id:
                regions = policy['regions']
                if regions != []:
                    x, y, w, h = regions
                    img = apply_crops(img, x, y, w, h)
                else:
                    pass
            iter_ = iter_ + 1
            ## save image by policy and add collection
            # Saving the frame
            save_path = consumer_mount_path + "/" + str(part_id) + "/frame" + str(frame_iter_) + str(iter_) + ".jpg"
            cv2.imwrite(save_path, img, [int(cv2.IMWRITE_JPEG_QUALITY), 90])  ##--- need to check this????
            img_path = str(part_id) + "/frame" + str(frame_iter_) + str(iter_) + ".jpg"

            capture_doc = {
                "file_path": img_path,
                "file_url": "http//0.0.0.0:3306/" + str(img_path),
                "state": "untagged",
                "annotation_detection": [],
                "annotation_detection_history": [],
                "annotation_classification": "",
                "annotation_classification_history": [],
                "annotator": ""}

            mp = MongoHelper().getCollection(part_id + "_dataset")
            mp.insert(capture_doc)

        print("\n\n")
        print(frame_iter_)
        frame_iter_ = frame_iter_ + 1
        logging.info('Received frame %s of part %s', frame_iter_, part_id)
    return 1


def start_camera_preview(workstation_id,camera_name):
    # access the workstation table
    workstation_id = ObjectId(workstation_id)
    mp = MongoHelper().getCollection(WORKSTATION_COLLECTION)
    ws_row = mp.find_one({'_id': workstation_id})
    ws_camera_dict = ws_row.get('cameras')
    
    for i in ws_camera_dict:
        camera_id = i['camera_id']
        camera_name1 = i['camera_name']
        if camera_name1 ==  camera_name:
            break
    
    topic = str(workstation_id) + "_" + str(camera_id)
    
    consumer = KafkaConsumer(topic, bootstrap_servers=KAFKA_BROKER_URL, auto_offset_reset='latest')
        
    for message in consumer:
        a = message.value.decode('utf-8')
        b = json.loads(a)
        
        im_b64_str = b["frame"]
        im_b64 = bytes(im_b64_str[2:], 'utf-8')
        im_binary = base64.b64decode(im_b64)

        im_arr = np.frombuffer(im_binary, dtype=np.uint8)
        img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
            

        ret, jpeg = cv2.imencode('.jpg', img)
        cv2.imwrite("frame.jpg", jpeg)
        
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


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




