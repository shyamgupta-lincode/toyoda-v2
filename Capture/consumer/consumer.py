# detector/app.py
import os
from time import sleep
from kafka import KafkaConsumer, KafkaProducer
import cv2
import numpy as np
import base64
import json
import pickle
from PIL import Image
import io
import logging
import sys
import pandas as pd
from pymongo import MongoClient


class mongo_client():
    def __init__(self, mongo_host, mongo_port):
        self.client = MongoClient(mongo_host, int(mongo_port))
        #self.db = self.client[collections_name]
        #self.db = ""
        #self.capture_table = self.db.capture
        #self.db_table = ""

    def add_to_metadata_collection(self, part_name, topic):
        # checking to see if part_name and gtopic is already registered???
        db = self.client["parts-metadata"]
        metadata_table = db.partsmetadata
        metadata_table.insert_one({"part_name": part_name, "topic": topic})
        # get part id for part name from collection
        #part_id =
        part_payload = metadata_table.find_one({"topic": topic})
        part_id = part_payload["_id"]
        return part_id

    def add_to_parts_collection(self, payload):
        db = self.client["parts-collection"]
        parts_table = db.parts
        parts_table.insert_one(payload)
        return


class Consumer():
    def __init__(self, KAFKA_BROKER_URL, topic, auto_offset_reset_value):
        self.obj = KafkaConsumer(topic, bootstrap_servers=KAFKA_BROKER_URL,
        value_deserializer=lambda value: json.loads(value), auto_offset_reset=auto_offset_reset_value, )
        self.topic = topic

    def collect_stream(self, mongo_client, part_id):
        print("\nReceiving\n")
        frame_iter_ = 0
        for message in self.obj:
            print(message.value)
            im_b64_str = message.value["frame"]
            im_b64 = bytes(im_b64_str[2:], 'utf-8')
            im_binary = base64.b64decode(im_b64)
            buf = io.BytesIO(im_binary)
            img = Image.open(buf)
            img_path = os.getcwd() + "/"+str(message.value["part"])+"/frame" + str(frame_iter_) + ".jpg"
            img.save(img_path)
            capture_doc = {
                "part_id": part_id,
                "image_path": img_path,
                "file_url": "",
                "state": "untagged",
                "regions": [],
                "regions_history": [],
                "annotations":"",
                "topic": self.topic,
                "part_name": str(message.value["part"]),
                "timestamp": pd.Timestamp.now()
            }
            print("\n\n")
            mongo_client.add_to_parts_collection(capture_doc)
            frame_iter_ = frame_iter_ + 1

            #Parts-Collection
            # collection_obj = {
            #     'file_path': os.path.join(settings.TRAIN_DATA_STATIC, name_of_img),
            #     'file_url': "http://164.52.194.78:3306/" + name_of_img,
            #     'state': 'untagged',
            #     'regions': [],
            #     'regions_history': [],
            #     'classifier_label': "",
            #     'classifier_label_history': [],
            #     'annotator': ''
            # }

    def close(self):
        self.obj.close()


if __name__ == "__main__":

    print("\nCreating WorkStation consumer by Part name\n")
    #KAFKA_BROKER_URL = "broker:9092"
    KAFKA_BROKER_URL = sys.argv[1]
    #mongo_host = 'mongodb'
    mongo_host = sys.argv[2]
    #mongo_port = 27017
    mongo_port = sys.argv[3]
    part_name = sys.argv[4]
    topic = sys.argv[5]
    consumer_ws = Consumer(KAFKA_BROKER_URL, topic, auto_offset_reset_value='earliest')
    ws_client = mongo_client(mongo_host, mongo_port)
    part_id = ws_client.add_to_metadata_collection(part_name, topic)
    os.mkdir(os.getcwd() + "/"+part_name)
    consumer_ws.collect_stream(ws_client, part_id)




