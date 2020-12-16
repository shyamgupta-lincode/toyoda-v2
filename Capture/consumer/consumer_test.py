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

KAFKA_BROKER_URL = "broker:9092"


class Consumer():
    def __init__(self, KAFKA_BROKER_URL, topic, auto_offset_reset_value):
        self.obj = KafkaConsumer(topic, bootstrap_servers=KAFKA_BROKER_URL,
        value_deserializer=lambda value: json.loads(value), auto_offset_reset=auto_offset_reset_value, )

    def collect_stream(self):
        print("\nReceiving\n")
        for message in self.obj:
            print(message.value["frame_idx"])
            im_b64_str = message.value["frame"]
            im_b64 = bytes(im_b64_str[2:], 'utf-8')
            im_binary = base64.b64decode(im_b64)
            buf = io.BytesIO(im_binary)
            img = Image.open(buf)
            img_path = os.getcwd() + "/data/frame" + str(message.value["frame_idx"]) + ".jpg"
            img.save(img_path)

    def close(self):
        self.obj.close()


if __name__ == "__main__":

    print("\nCreating WorkStation 1\n")
    topic = "WorkStation1"
    consumer_ws = Consumer(KAFKA_BROKER_URL, topic, auto_offset_reset_value='earliest')

    consumer_ws.collect_stream()

    # consumer1 = KafkaConsumer(
    #      "WorkStation1",
    #      bootstrap_servers=KAFKA_BROKER_URL,
    #      value_deserializer=lambda value: json.loads(value),
    #      auto_offset_reset='earliest',
    # )

    ### For accepting single frame by topic ---
    # for message in consumer1:
    #      print(message.value)
    #      im_b64_str = message.value["key"]
    #      im_b64 = bytes(im_b64_str[2:], 'utf-8')
    #      im_binary = base64.b64decode(im_b64)
    #      buf = io.BytesIO(im_binary)
    #      img = Image.open(buf)
    #      img.save("result_video.jpg")


    ### For accepting video by topic ---

    # for message in consumer1:
    #     # print(message.value["frame"])
    #     # print("\n\n\n")
    #     # print(message.value["part"])
    #     # print("\n\n\n")
    #     # print(message.value["frame_idx"])
    #     # print("\n\n\n")
    #     im_b64_str = message.value["frame"]
    #     im_b64 = bytes(im_b64_str[2:], 'utf-8')
    #     im_binary = base64.b64decode(im_b64)
    #     buf = io.BytesIO(im_binary)
    #     img = Image.open(buf)
    #     #print(os.getcwd())
    #     img_path = os.getcwd()+"/data/frame"+str(message.value["frame_idx"])+".jpg"
    #     img.save(img_path)





