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

KAFKA_BROKER_URL = "broker:9092"


class mongo_client():
    def __init__(self, collections_name):
        self.client = MongoClient('mongodb', 27017)
        self.db = self.client[collections_name]
        self.capture_table = self.db.capture

    def insert_doc(self, payload):
        self.capture_table.insert_one(payload)
        return


class Consumer():
    def __init__(self, KAFKA_BROKER_URL, topic, auto_offset_reset_value):
        self.obj = KafkaConsumer(topic, bootstrap_servers=KAFKA_BROKER_URL,
        value_deserializer=lambda value: json.loads(value), auto_offset_reset=auto_offset_reset_value, )
        self.topic = topic

    def collect_stream(self, mongo_client):
        print("\nReceiving\n")
        frame_iter_ = 0
        for message in self.obj:
            im_b64_str = message.value["frame"]
            im_b64 = bytes(im_b64_str[2:], 'utf-8')
            im_binary = base64.b64decode(im_b64)
            buf = io.BytesIO(im_binary)
            img = Image.open(buf)
            img_path = os.getcwd() + "/data/frame" + str(frame_iter_) + ".jpg"
            img.save(img_path)
            capture_doc = {
                "image_path": img_path,
                "topic": self.topic,
                "part_name": str(message.value["part"]),
                "timestamp": pd.Timestamp.now()
            }
            print("\n\n")
            mongo_client.insert_doc(capture_doc)
            frame_iter_ = frame_iter_ + 1

    def close(self):
        self.obj.close()


if __name__ == "__main__":

    print("\nCreating WorkStation 1\n")
    topic = sys.argv[1]
    consumer_ws = Consumer(KAFKA_BROKER_URL, topic, auto_offset_reset_value='earliest')
    ws_client = mongo_client("capture-collections")
    consumer_ws.collect_stream(ws_client)




