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


class Consumer():
    def __init__(self, KAFKA_BROKER_URL, topic, auto_offset_reset_value):
        self.obj = KafkaConsumer(topic, bootstrap_servers=KAFKA_BROKER_URL,
        value_deserializer=lambda value: json.loads(value), auto_offset_reset=auto_offset_reset_value,)
        self.topic = topic

    def collect_bulk_upload_data(self):
        print("\n Receiving results after inference\n")
        logging.info('Receiving results after inference')
        im_str = ""
        for message in self.obj:
            print("\n\n")
            print(message.value)
            if message.value["frame"] == "END":
                im_b64 = bytes(im_str[2:], 'utf-8')
                im_binary = base64.b64decode(im_b64)
                buf = io.BytesIO(im_binary)
                img = Image.open(buf)
                # Saving the frame
                img_path = os.getcwd() + "/" + str(message.value["part"]) + "/frame" + \
                           str(message.value["frame_idx"]) + "."+str(message.value["file_format"])
                img.save(img_path)
            if im_str == "END":
                im_str = ""
            else:
                im_str = im_str + message.value["frame"]
            logging.info('Received frame %s of part %s', message.value["frame_idx"], message.value["part"])

    def close(self):
        self.obj.close()


if __name__ == "__main__":
    # Creating a logging object
    logging.basicConfig(filename='Status.log',
                        level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    print("\nCreating WorkStation consumer by Part name\n")
    logging.info('Creating WorkStation consumer by Part name')
    KAFKA_BROKER_URL = sys.argv[1]
    mongo_host = sys.argv[2]
    mongo_port = sys.argv[3]
    topic = sys.argv[4]
    part_name = sys.argv[5]
    os.mkdir(os.getcwd() + "/" + part_name)
    # Creating a Kafka consumer
    consumer_ws = Consumer(KAFKA_BROKER_URL, topic, auto_offset_reset_value='earliest')
    consumer_ws.collect_bulk_upload_data()




