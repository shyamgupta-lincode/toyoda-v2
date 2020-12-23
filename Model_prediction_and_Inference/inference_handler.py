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
from tf_engine import *

# Add the mongo part -------


class Consumer():
    def __init__(self, KAFKA_BROKER_URL, topic, auto_offset_reset_value):
        self.obj = KafkaConsumer(topic, bootstrap_servers=KAFKA_BROKER_URL,
        value_deserializer=lambda value: json.loads(value), auto_offset_reset=auto_offset_reset_value, )
        self.topic = topic

    def collect_stream(self, mongo_client, part_id, inference_object, producer_to_camera_service):
        print("\nReceiving the stream images\n")
        frame_iter_ = 0
        for message in self.obj:
            # Decoding the image stream
            im_b64_str = message.value["frame"]
            im_b64 = bytes(im_b64_str[2:], 'utf-8')
            im_binary = base64.b64decode(im_b64)
            buf = io.BytesIO(im_binary)
            img = Image.open(buf)
            # Saving the frame
            img_path = os.getcwd() + "/"+str(message.value["part"])+"/frame" + str(frame_iter_) + ".jpg"
            img.save(img_path)
            # add to collections -----

            # perform inference -----
            out = inference_object.DetectFromImage(img_path)
            print("\nResults of Inference for frame"+str(frame_iter_)+"\n")
            print(out)
            # publish to results topic -------
            payload = {
                "part": message.value["part"],
                "result": out
            }
            producer_to_camera_service.publish_result(payload)
            frame_iter_ = frame_iter_ + 1

    def close(self):
        self.obj.close()


class Producer():
    def __init__(self, KAFKA_BROKER_URL, topic):
        self.obj = KafkaProducer(bootstrap_servers=KAFKA_BROKER_URL,
                             value_serializer=lambda value: json.dumps(value).encode(), )
        self.topic = topic

    def publish_result(self, payload):
        self.obj.send(self.topic, value=payload)
        return 0


if __name__ == "__main__":
    print("\nCreating Inference consumer by topic\n")
    KAFKA_BROKER_URL = sys.argv[1]
    mongo_host = sys.argv[2]
    mongo_port = sys.argv[3]
    part_name = sys.argv[4]
    topic = sys.argv[5]
    #model_path = "saved_model"
    model_path  = sys.argv[6]
    #label_path = "labels.txt"
    label_path = sys.argv[7]
    topic_to_camera_service_for_results = sys.argv[8]
    # Creating a Kafka consumer
    consumer_ws = Consumer(KAFKA_BROKER_URL, topic, auto_offset_reset_value='earliest')
    # Creating a mongo client to store collections----------
    # Inference consumer receives the stream, performs inference and publishes to topic
    mongo_client = ""
    os.mkdir(os.getcwd() + "/" + part_name)
    # Load the model for inference
    inf_obj = DetectorTF2(model_path, label_path)
    producer_for_results = Producer(KAFKA_BROKER_URL, topic_to_camera_service_for_results)
    consumer_ws.collect_stream(mongo_client, part_name, inf_obj, producer_for_results)
