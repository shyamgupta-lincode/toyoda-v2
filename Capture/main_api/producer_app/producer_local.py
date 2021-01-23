import sys
import cv2
import neoapi
import time
import datetime
import os
import time
import base64
import cv2
from kafka import KafkaProducer
import json
import logging
import pymongo

class Producer():
    """
        Publishes video data from camera to topic
    """
    def __init__(self, KAFKA_BROKER_URL, topic):
        """
        Instantiates the Producer object

        Arguments:
            KAFKA_BROKER_URL: url to connect to Broker
            part: part id/name that is being captured
            topic: topic to publish video stream to
        """
        self.obj = KafkaProducer(bootstrap_servers=KAFKA_BROKER_URL,
                             value_serializer=lambda value: json.dumps(value).encode(), )
        self.topic = topic


    def stream_video(self, camera_index):
        """
        Accesses frames from the camera, encodes it and publishes it to the respective topic

        Arguments:
            file_format: format of the image data to be sent to the Kafka consumer
        """
        camera = neoapi.Cam()
        print(camera.Connect(camera_index))

        time.sleep(2)
        width = 1280
        height = 720
        start = datetime.datetime.now()
        while True:
            img = camera.GetImage().GetNPArray()

            if len(img) == 0:
                time.sleep(0.2)
                continue
            img = cv2.resize(img, (width, height))
            stop = datetime.datetime.now()
            print(stop - start)
            title = 'Press [ESC] to exit ..'
            start = datetime.datetime.now()
            im_b64 = base64.b64encode(img)
            payload_video_frame = {"frame": str(im_b64)}
            self.obj.send(self.topic, value=payload_video_frame)
            time.sleep(1)
        return 0



### Access the mongo collection for wid cameraname
wid = "123"
camera_id = "0"
#### Create kafka topic wid_camera_id
topic = wid +camera_id
KAFKA_BROKER_URL = "broker:9092"
producer_ws = Producer(KAFKA_BROKER_URL, topic)

logging.info('Initiating the stream')
status_code = producer_ws.stream_video(camera_id)
logging.info('Done streaming')




