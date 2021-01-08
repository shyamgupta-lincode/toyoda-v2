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
import shutil
import time


class Producer():
    """
        Publishes video data from camera to topic
    """
    def __init__(self, KAFKA_BROKER_URL, part, topic):
        """
        Instantiates the Producer object

        Arguments:
            KAFKA_BROKER_URL: url to connect to Broker
            part: part id/name that is being captured
            topic: topic to publish video stream to
        """
        self.obj = KafkaProducer(bootstrap_servers=KAFKA_BROKER_URL,
                             value_serializer=lambda value: json.dumps(value).encode(), )
        self.part = part
        self.topic = topic

    def extract_zipfile(self, compressed_file_path, archive_format):
        """
        Extracts files from compressed folder based on the

        Arguments:
            compressed_file_path: location of the compressed folder to be extracted
            archive_format: format of the compressed folder

        Returns:
            extracted_img_path: Folder containing the extracted image files
        """
        logging.info('Extracting all the files now...')
        # one of “zip”, “tar”, “gztar”, “bztar”, or “xztar”
        if archive_format in ["zip", "tar", "gztar", "bztar", "xztar"]:
            shutil.unpack_archive(compressed_file_path)
        elif archive_format == "gzip":
            # need to add
            print(".")
        logging.info('Done extracting files!')
        ind_ = compressed_file_path.find(".")
        extracted_img_path = compressed_file_path[:ind_]
        logging.info('extracted image path is %s', extracted_img_path)
        return extracted_img_path

    def encode_data_for_streaming(self, extracted_img_path, filename):
        """
        Encode data to be streamed to consumer

        Arguments:
            extracted_img_path: Folder containing the extracted files
            filename: Image file name to be encoded

        Returns:
            img_str: endcoded image data
        """
        with open(os.getcwd() + "/" + extracted_img_path + "/" + filename, 'rb') as f:
            im_b64 = base64.b64encode(f.read())
            img_str = str(im_b64)
        return img_str

    def stream_data(self, compressed_file_path, archive_format, file_format):
        """
        extracts image files from folder, encodes and publishes to topic

        Arguments:
            compressed_file_path: Path to folder to be extracted
            archive_format: Format of the folder to extracted can be  “zip”, “tar”, “gztar”, “bztar”, or “xztar”
            file_format: format of the image data to be sent to the Kafka consumer

        """
        extracted_img_path = self.extract_zipfile(compressed_file_path, archive_format)
        frames_iter = 1
        for filename in os.listdir(extracted_img_path):
            img_str = ""
            buf_str = ""
            img_str = self.encode_data_for_streaming(extracted_img_path, filename)
            i = 0
            while i <= len(img_str)-1:
                buf_str = img_str[i:i+10000]
                payload = {"frame": buf_str, "part": self.part, "frame_idx": frames_iter, "file_format": file_format}
                self.obj.send(self.topic, value=payload)
                time.sleep(1)
                i = i+10000
            payload = {"frame": "END", "part": self.part, "frame_idx": frames_iter, "file_format": file_format}
            self.obj.send(self.topic, value=payload)
            logging.info('Sending frame %s of part %s', frames_iter, self.part)
            frames_iter = frames_iter + 1
            time.sleep(1)
        return 0


if __name__ == "__main__":
        # Creating a logging object
        logging.basicConfig(filename='Status.log',
                        level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
        zip_file_path = sys.argv[1]
        archive_format = sys.argv[2]
        part = sys.argv[3]
        topic = sys.argv[4]
        KAFKA_BROKER_URL = sys.argv[5]
        file_format = sys.argv[6]
        logging.info('Creating the Producer object for streaming')
        producer_ws = Producer(KAFKA_BROKER_URL, part, topic)
        logging.info('Initiating the stream')
        producer_ws.stream_data(zip_file_path, archive_format, file_format)
        logging.info('Done streaming')

