import os
from kafka import KafkaProducer
import json
import cv2
import numpy as np
import base64
import time
from PIL import Image
import sys


class Producer():
    def __init__(self, KAFKA_BROKER_URL, video_input, part, topic):
        self.obj = KafkaProducer(bootstrap_servers=KAFKA_BROKER_URL,
                             value_serializer=lambda value: json.dumps(value).encode(), )
        self.video_input = video_input
        self.part = part
        self.topic = topic

    def stream_video(self):
        cap = cv2.VideoCapture(self.video_input)
        frames_iter = 0
        while (cap.isOpened()):
            ret, frame = cap.read()
            if ret == True:
                frames_iter = frames_iter + 1
                cv2.imwrite("tmp.jpg", frame)
                with open("tmp.jpg", 'rb') as f:
                    im_b64 = base64.b64encode(f.read())
                payload_video_frame = {"frame": str(im_b64), "part": self.part, "frame_idx": frames_iter}
                self.obj.send(self.topic, value=payload_video_frame)
                print(payload_video_frame["frame_idx"])
            else:
                break
        cap.release()
        return 0


if __name__ == "__main__":
        ## Can be live video capture
        ## Can be RTSP input
        #video_input = 'part_abc.mp4'
        video_input = sys.argv[1]
        part = sys.argv[2]
        topic = sys.argv[3]
        #KAFKA_BROKER_URL = "broker:9092"
        KAFKA_BROKER_URL = sys.argv[4]

        print("\nCreating WorkStation\n")
        producer_ws = Producer(KAFKA_BROKER_URL, video_input, part, topic)
        producer_ws.stream_video()
        print("\nDone streaming\n")
