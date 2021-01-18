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
from MongoHelper import *
from common.utils import MongoHelper

KAFKA_BROKER_URL = "broker:9092"
consumer_mount_path = "/Livis"
ws_client = mongo_client(mongo_host, mongo_port)

def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance


class Consumer():
    """
    Receives the image feed form the subscribed topic
    """
    def __init__(self, KAFKA_BROKER_URL, topic, auto_offset_reset_value):
        """
        Instantiates the Consumer object

        Arguments:
            KAFKA_BROKER_URL: url to connect to Kafka Broker
            topic: topic to subscribe the video frame from
            auto_offset_reset_value: What to do when there is no initial offset in Kafka or if the current offset \
            does not exist any more on the server (e.g. because that data has been deleted):
        """
        self.obj = KafkaConsumer(topic, bootstrap_servers=KAFKA_BROKER_URL,
        value_deserializer=lambda value: json.loads(value), auto_offset_reset=auto_offset_reset_value,)
        self.topic = topic

    def collect_stream(self, part_id, workstation_id):
        """"
        Receives the encoded image frames from the prescribed topic

        Arguments:
            mongo_client: client to access the mongo server
            part_id: part name/id being captured in the image frames

        """
        logging.info("\nReceiving the stream images\n")
        frame_iter_ = 0
        for message in self.obj:
            # Decoding the image stream
            im_b64_str = message.value["frame"]
            im_b64 = bytes(im_b64_str[2:], 'utf-8')
            im_binary = base64.b64decode(im_b64)

            im_arr = np.frombuffer(im_binary, dtype=np.uint8)
            img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
            # Saving the frame
            img_path = consumer_mount_path + "/" + str(part_id) + "/frame" + str(frame_iter_) + ".png"

            cv2.imwrite(img_path, img)

            capture_doc = {
                "part_id": part_id,
                "image_path": img_path,
                "workstation_id": workstation_id,
                "topic": self.topic,
                "timestamp": pd.Timestamp.now()
            }
            print("\n\n")
            ws_client.add_to_parts_collection(capture_doc)
            print(frame_iter_)
            frame_iter_ = frame_iter_ + 1
            logging.info('Received frame %s of part %s', frame_iter_, message.value["part"])

    def collect_bulk_upload_data(self, part_id, workstation_id, mongo_client, img_database_path):
        """
        Receives the encoded image frames from the prescribed topic

        Arguments:
            mongo_client: client to access the mongo server
            part_id: id of the part from "parts metadata" collection being captured in the image frames
            part_name: part name being captured in the image stream

        """
        print("\n Receiving results after inference\n")
        logging.info('Receiving results after inference')
        im_str = ""
        frames_iter = 0
        for message in self.obj:
            print("\n\n")
            print(message.value)
            if message.value["frame"] == "END":
                im_b64 = bytes(im_str[2:], 'utf-8')
                im_binary = base64.b64decode(im_b64)
                im_arr = np.frombuffer(im_binary, dtype=np.uint8)
                img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
                # Saving the frame
                img_path = img_database_path + "/frame" + \
                           str(frames_iter) + ".png"
                cv2.imwrite(img_path, img)

                capture_doc = {
                    "part_id": part_id,
                    "image_path": img_path,
                    "file_url": "",
                    "state": "untagged",
                    "regions": [],
                    "regions_history": [],
                    "annotations": "",
                    "topic": self.topic,
                    "part_name": part_name,
                    "timestamp": pd.Timestamp.now()
                }

                mongo_client.add_to_parts_collection(capture_doc)
                frames_iter = frames_iter + 1
            if im_str == "END":
                im_str = ""
            else:
                im_str = im_str + message.value["frame"]
            logging.info('Received frame %s of part %s', message.value["frame_idx"], message.value["part"])


    def close(self):
        self.obj.close()




def start_bulk_upload_stream(data):
    #Creating a logging object
    logging.basicConfig(filename='Status.log',
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

    logging.info('Creating the Consumer object for streaming')

    topic = str(part_id) + str(workstation_id)

    try:
        consumer = Consumer(KAFKA_BROKER_URL, topic, auto_offset_reset_value='earliest')
    except:
        message = "Consumer object creation failed"
        status_code = 415
        return message, status_code

    # Streaming the frames
    logging.info('Initiating the consumer')
    # Registering the part name to parts-metadata collection
    part_id = ws_client.add_to_metadata_collection(part_name, topic)
    # Creating a folder to store the images consumed, folder name is part name
    img_database_path = consumer_mount_path + "/" + str(part_id)
    if os.path.exists(img_database_path):
        pass
    else:
        os.makedirs(img_database_path)

    status_code = consumer.collect_bulk_upload_data(part_id, workstation_id, ws_client, img_database_path)
    logging.info('Done receiving streaming')
    message = "Done receiving streaming"
    status_code = 200
    return message, status_code


def start_video_stream(data):

    logging.basicConfig(filename='Status.log',
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
        camera_indexes = data['camera_indexes']
    except:
        message = "camera indexes not provided"
        status_code = 400
        return message, status_code

    logging.info('Creating the Producer object for streaming')

    for id in camera_indexes:
        topic = str(part_id) + str(workstation_id)
        try:
            consumer = Consumer(KAFKA_BROKER_URL, topic)
        except:
            message = "Consumer object creation failed"
            status_code = 415
            return message, status_code

        # Streaming the frames
        logging.info('Initiating the consumer')

        status_code = consumer.collect_stream(part_id, workstation_id)
        logging.info('Done receiving streaming')
        message = "Done receiving streaming"
        status_code = 200
        return message, status_code
