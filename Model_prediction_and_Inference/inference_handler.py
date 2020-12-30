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
import logging


class Producer():
    def __init__(self, KAFKA_BROKER_URL, topic):
        self.obj = KafkaProducer(bootstrap_servers=KAFKA_BROKER_URL,
                             value_serializer=lambda value: json.dumps(value).encode(), )
        self.topic = topic

    def infer_and_publish_results(self, img_file_path, inf_obj):
        for filename in os.listdir(img_file_path):
            logging.info('currently processing %s', filename)
            out = inf_obj.DetectFromImage(img_file_path+"/"+filename)
            # publish to results topic -------
            payload = {
                "filename": filename,
                "result": out
            }
            self.obj.send(self.topic, value=payload)
        return 0


if __name__ == "__main__":
    # Creating a logging object
    logging.basicConfig(filename='Status_of_Output_Stream.log',
                        level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    logging.info('Starting the Inference handler')
    KAFKA_BROKER_URL = sys.argv[1]
    mongo_host = sys.argv[2]
    mongo_port = sys.argv[3]
    part_name = sys.argv[4]
    topic = sys.argv[5]
    model_path = sys.argv[6]
    label_path = sys.argv[7]
    topic_to_camera_service_for_results = sys.argv[8]
    # Creating a mongo client to store collections----------
    # Inference consumer performs inference on stored image data and publishes to topic
    logging.info('Creating a producer object')
    img_file_path = "/apps/Capture/consumer/" + part_name
    producer = Producer(KAFKA_BROKER_URL, topic_to_camera_service_for_results)
    # Load the model for inference
    inf_obj = DetectorTF2(model_path, label_path)
    logging.info('Infering and publish results')
    producer.infer_and_publish_results(img_file_path, inf_obj)
