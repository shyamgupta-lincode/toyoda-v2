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
        value_deserializer=lambda value: json.loads(value), auto_offset_reset=auto_offset_reset_value, )
        self.topic = topic

    def collect_inference_results(self):
        print("\n Receiving results after inference\n")
        for message in self.obj:
            print("\n")
            print(message.value)
            print("\n")

    def close(self):
        self.obj.close()


if __name__ == "__main__":

    print("\nCreating WorkStation consumer by Part name\n")
    KAFKA_BROKER_URL = sys.argv[1]
    mongo_host = sys.argv[2]
    mongo_port = sys.argv[3]
    topic = sys.argv[4]
    # Creating a Kafka consumer
    consumer_ws = Consumer(KAFKA_BROKER_URL, topic, auto_offset_reset_value='earliest')
    consumer_ws.collect_inference_results()




