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

KAFKA_BROKER_URL = "broker:9092"


class Consumer():
    def __init__(self, KAFKA_BROKER_URL, topic, auto_offset_reset_value):
        self.obj = KafkaConsumer(topic, bootstrap_servers=KAFKA_BROKER_URL,
        value_deserializer=lambda value: json.loads(value), auto_offset_reset=auto_offset_reset_value, )

    def collect_stream(self):
        print("\nReceiving\n")
        for message in self.obj:
            print("\n")
            print(message.value)

    def close(self):
        self.obj.close()


if __name__ == "__main__":
    topic = sys.argv[1]
    consumer_ws = Consumer(KAFKA_BROKER_URL, topic, auto_offset_reset_value='earliest')
    consumer_ws.collect_stream()
