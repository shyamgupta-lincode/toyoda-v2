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
#from common.utils import MongoHelper

KAFKA_BROKER_URL = "broker:9092"
consumer_mount_path = "/apps/Livis"
mongo_host = "mongodb"
mongo_port = "27017"

def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance


class mongo_client():
    """
    Creates a mongo client for accessing and performing operations on a mongo database that is hosted on a mongo server
    """

    def __init__(self, mongo_host, mongo_port):
        """
        Instantiates a pymongo client fir interacting with the mongo database

        Arguments:
            mongo_host: host for connecting to the server hosting the mongo server
            mongo_port: port for connecting to the server hosting the mongo server
        """
        self.client = MongoClient(mongo_host, int(mongo_port))

    def add_to_metadata_collection(self, part_name, topic):
        """"
        Registers the part id/name to the "parts metadata" collection

        Arguments:
            part_name: part to be registered
            topic: topic that the consumer receives the images for the given part

        """
        db = self.client["parts-metadata"]
        metadata_table = db.partsmetadata
        metadata_table.insert_one({"part_name": part_name, "topic": topic})
        part_payload = metadata_table.find_one({"topic": topic})
        part_id = part_payload["_id"]
        return part_id

    def add_to_parts_collection(self, payload):
        """
        Records the image data received for the given topic

        Arguments:
            payload: Collection to be added to the "parts collection"
        """
        db = self.client["parts-collection"]
        parts_table = db.parts
        parts_table.insert_one(payload)
        return



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

    def collect_stream(self, part_id, workstation_id, ws_client):
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
            print(img_path)
            cv2.imwrite(img_path, img)

            capture_doc = {
                "part_id": part_id,
                "image_path": img_path,
                "workstation_id": workstation_id,
                "topic": self.topic,
                "camera_id": message.value["camera_index"],
                "timestamp": pd.Timestamp.now()
            }
            print("\n\n")
            #ws_client.add_to_parts_collection(capture_doc)
            print(frame_iter_)
            frame_iter_ = frame_iter_ + 1
            logging.info('Received frame %s of part %s', frame_iter_, part_id)


    def close(self):
        self.obj.close()




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

    logging.info('Creating the Consumer object for streaming')

    topic = str(part_id) + str(workstation_id)
    # Registering the part name to parts-metadata collection
    ws_client = ""
    #ws_client = mongo_client(mongo_host, mongo_port)
    #part_id = ws_client.add_to_metadata_collection(part_id, topic)
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

    status_code = consumer.collect_stream(part_id, workstation_id, ws_client)
    logging.info('Done receiving streaming')
    message = "Done receiving streaming"
    status_code = 200
    return message, status_code
