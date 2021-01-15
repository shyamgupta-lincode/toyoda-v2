import os
from kafka import KafkaProducer
import json
import cv2
import numpy as np
import base64
import time
import sys
import logging
import shutil


class Producer():
    """
        Publishes video data from camera to topic
    """
    def __init__(self, KAFKA_BROKER_URL, part, topic, image_path=""):
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
        self.image_path = image_path

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
            ind_ = compressed_file_path.find(".")
            extracted_dir = compressed_file_path[:ind_]
            shutil.unpack_archive(compressed_file_path, extracted_dir, archive_format)
        elif archive_format == "gzip":
            # need to add
            print(".")
        logging.info('Done extracting files!')
        logging.info('extracted image path is %s', extracted_dir)
        return extracted_dir

    def encode_data_for_streaming(self, extracted_img_path, filename):
        """
        Encode data to be streamed to consumer

        Arguments:
            extracted_img_path: Folder containing the extracted files
            filename: Image file name to be encoded

        Returns:
            img_str: endcoded image data
        """
        with open(extracted_img_path + "/" + filename, 'rb') as f:
            im_b64 = base64.b64encode(f.read())
            img_str = str(im_b64)
        return img_str

    def stream_bulk_upload_data(self, compressed_file_path, archive_format, file_format):
        """
        extracts image files from folder, encodes and publishes to topic

        Arguments:
            compressed_file_path: Path to folder to be extracted
            archive_format: Format of the folder to extracted can be  “zip”, “tar”, “gztar”, “bztar”, or “xztar”
            file_format: format of the image data to be sent to the Kafka consumer

        """
        extracted_dir = self.extract_zipfile(compressed_file_path, archive_format)
        extracted_img_path = extracted_dir + "/" + self.part
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

    def stream_video(self, file_format, frames_iter):
        """
        Accesses frames from the camera, encodes it and publishes it to the respective topic

        Arguments:
            file_format: format of the image data to be sent to the Kafka consumer
        """

        with open(self.image_path, 'rb') as f:
            im_b64 = base64.b64encode(f.read())
        payload_video_frame = {"frame": str(im_b64), "part": self.part, "frame_idx": frames_iter,\
                                    "file_format": file_format}
        print("\n\n")
        print(payload_video_frame)
        self.obj.send(self.topic, value=payload_video_frame)
        time.sleep(1)
        # cap = cv2.VideoCapture(self.video_input)
        # frames_iter = 0
        # while (cap.isOpened()):
        #     ret, frame = cap.read()
        #     if ret == True:
        #         frames_iter = frames_iter + 1
        #         # Encoding and sending the frame
        #         cv2.imwrite("tmp.jpg", frame)
        #         with open("tmp.jpg", 'rb') as f:
        #             im_b64 = base64.b64encode(f.read())
        #         payload_video_frame = {"frame": str(im_b64), "part": self.part, "frame_idx": frames_iter,\
        #                                "file_format": file_format}
        #         self.obj.send(self.topic, value=payload_video_frame)
        #         time.sleep(1)
        #     else:
        #         break
        # cap.release()
        return 0


def start_bulk_upload_stream(data):
    #Creating a logging object
    logging.basicConfig(filename='Status.log',
                         level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    try:
        compressed_file_path = data['compressed_file_path']
    except:
        message = "File path not found"
        status_code = 400
        return message, status_code

    try:
        compression_format = data['compression_format']
    except:
        message = "Compression format not provided"
        status_code = 400
        return message, status_code

    try:
        part = data['part_name']
    except:
        message = "part name not provided"
        status_code = 400
        return message, status_code

    try:
        topic = data['topic']
    except:
        message = "Topic not provided"
        status_code = 400
        return message, status_code

    try:
        KAFKA_BROKER_URL = data['broker_url']
    except:
        message = "Broker url not provided"
        status_code = 400
        return message, status_code

    try:
        file_format = data['file_format']
    except:
        message = "image file format not provided"
        status_code = 400
        return message, status_code
    logging.info('Creating the Producer object for streaming')

    try:
        producer_ws = Producer(KAFKA_BROKER_URL, part, topic)
    except:
        message = "Producer object creation failed"
        status_code = 415
        return message, status_code

    logging.info('Initiating the stream')
    producer_ws.stream_bulk_upload_data(compressed_file_path, compression_format, file_format)
    logging.info('Done streaming')
    message = "Done streaming"
    status_code = 200
    return message, status_code


def start_video_stream(data):

    logging.basicConfig(filename='Status.log',
                        level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

    try:
        image_path = data['image_path']
    except:
        message = "image path not provided"
        status_code = 400
        return message, status_code
        
    try:
        part_name = data['part_name']
    except:
        message = "part name not provided"
        status_code = 400
        return message, status_code

    try:
        topic = data['topic']
    except:
        message = "topic not provided"
        status_code = 400
        return message, status_code

    try:
        KAFKA_BROKER_URL = data['broker_url']
    except:
        message = "Broker url not provided"
        status_code = 400
        return message, status_code

    try:
        file_format = data['image_file_format']
    except:
        message = "Image file format not provided"
        status_code = 400
        return message, status_code

    try:
        frames_iter = data['frames_iter']
    except:
        message = "Frame count not provided"
        status_code = 400
        return message, status_code

    logging.info('Creating the Producer object for streaming')

    try:
        producer_ws = Producer(KAFKA_BROKER_URL, part_name, topic, image_path)
    except:
        message = "Producer object creation failed"
        status_code = 415
        return message, status_code

    print(producer_ws)

    # Streaming the frames
    logging.info('Initiating the stream')

    producer_ws.stream_video(file_format, frames_iter)
    logging.info('Done streaming')
    message = "Done streaming"
    status_code = 200
    return message, status_code
