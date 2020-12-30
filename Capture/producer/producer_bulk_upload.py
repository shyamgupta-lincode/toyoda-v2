import os
from kafka import KafkaProducer
import json
import cv2
import numpy as np
import base64
import time
from PIL import Image
import sys
from zipfile import ZipFile
import logging


class Producer():
    def __init__(self, KAFKA_BROKER_URL, zip_file_path, part, topic):
        self.obj = KafkaProducer(bootstrap_servers=KAFKA_BROKER_URL,
                             value_serializer=lambda value: json.dumps(value).encode(), )
        self.file_path = zip_file_path
        self.part = part
        self.topic = topic

    def extract_zipfile(self):
        with ZipFile(self.file_path, 'r') as zip:
            # extracting all the files
            logging.info('Extracting all the files now...')
            zip.extractall()
            logging.info('Done extracting files!')
        file_name_ind = self.file_path.find(".")
        extracted_img_path = self.file_path[:file_name_ind]
        logging.info('extracted image path is %s', extracted_img_path)
        return extracted_img_path

    def stream_files(self):
        extracted_img_path = self.extract_zipfile()
        frames_iter = 1
        for filename in os.listdir(extracted_img_path):
            logging.info('processing filename %s', filename)
            with open(os.getcwd()+"/"+extracted_img_path+"/"+filename, 'rb') as f:
                im_b64 = base64.b64encode(f.read())
            payload = {"frame": str(im_b64), "part": self.part, "frame_idx": frames_iter}
            self.obj.send(self.topic, value=payload)
            frames_iter = frames_iter + 1
        return 0


if __name__ == "__main__":
        # Creating a logging object
        logging.basicConfig(filename='Status_of_Bulk_upload_producer.log',
                        level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
        zip_file_path = sys.argv[1]
        part = sys.argv[2]
        topic = sys.argv[3]
        KAFKA_BROKER_URL = sys.argv[4]
        logging.info('Creating the Producer object for streaming')
        producer_ws = Producer(KAFKA_BROKER_URL, zip_file_path, part, topic)
        logging.info('Initiating the stream')
        producer_ws.stream_files()
        logging.info('Done streaming')

