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
from common.utils import MongoHelper
import multiprocessing

KAFKA_BROKER_URL = "broker:9092"

def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance


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

    def stream_bulk_upload_data(self, compressed_file_path, archive_format, part_id, workstation_id):
        """
        extracts image files from folder, encodes and publishes to topic

        Arguments:
            compressed_file_path: Path to folder to be extracted
            archive_format: Format of the folder to extracted can be  “zip”, “tar”, “gztar”, “bztar”, or “xztar”
            file_format: format of the image data to be sent to the Kafka consumer

        """
        extracted_dir = self.extract_zipfile(compressed_file_path, archive_format)
        extracted_img_path = extracted_dir + "/" + part_id
        frames_iter = 1
        for filename in os.listdir(extracted_img_path):
            with open(filename, 'rb') as f:
                im_b64 = base64.b64encode(f.read())
            payload = {"frame": str(im_b64), "camera_index":"", "frame_idx": frames_iter}
            self.obj.send(self.topic, value=payload)
            time.sleep(1)

        return 0

    def stream_video(self, part_id, workstation_id, camera_index):
        """
        Accesses frames from the camera, encodes it and publishes it to the respective topic

        Arguments:
            file_format: format of the image data to be sent to the Kafka consumer
        """

        ### Code to check if camera id is valid

        cap = cv2.VideoCapture(camera_index)
        frames_iter = 0
        while (cap.isOpened()):
             ret, frame = cap.read()
             if ret == True:
                 frames_iter = frames_iter + 1
                 # Encoding and sending the frame
                 cv2.imwrite("tmp.jpg", frame)
                 with open("tmp.jpg", 'rb') as f:
                     im_b64 = base64.b64encode(f.read())
                 payload_video_frame = {"frame": str(im_b64), "camera_index": str(camera_index),
                                        "frames_iter": str(frames_iter)}
                 self.obj.send(self.topic, value=payload_video_frame)
                 time.sleep(1)
             else:
                 break
        cap.release()
        return 200


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
        part_id = data['part_id']
    except:
        message = "part id not provided"
        status_code = 400
        return message, status_code

    try:
        workstation_id = data['workstation_id']
    except:
        message = "Workstation ID not provided"
        status_code = 400
        return message, status_code

    logging.info('Creating the Producer object for streaming')

    topic = str(part_id) + str(workstation_id)

    try:
        producer_ws = Producer(KAFKA_BROKER_URL, topic)
    except:
        message = "Producer object creation failed"
        status_code = 415
        return message, status_code

    logging.info('Initiating the stream')
    producer_ws.stream_bulk_upload_data(compressed_file_path, compression_format, part_id, workstation_id)
    logging.info('Done streaming')
    message = "Done streaming"
    status_code = 200
    return message, status_code


def start_video_stream(data):

    logging.basicConfig(filename='Status.log',
                        level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

    try:
        part_id = data['part_id']
    except:
        message = "part id not provided"
        status_code = 400
        return message, status_code
        
    try:
        workstation_id = data['workstation_id']
    except:
        message = "workstation id not provided"
        status_code = 400
        return message, status_code

    try:
        camera_indexes = data['camera_indexes']
    except:
        message = "camera indexes not provided"
        status_code = 400
        return message, status_code

    logging.info('Creating the Producer object for streaming')
    jobs = []

    for id in camera_indexes:
        topic = str(part_id) + str(workstation_id)
        p = multiprocessing.Process(target=start_multiprocess_stream, args=(KAFKA_BROKER_URL, topic, part_id,
                                                                            workstation_id, id))
        p.start()
        jobs.append(p)
        p.join()

    for job in jobs:
        if job.exitcode != 0:
            status_code = 400
            message = "Failed streaming"
            return status_code, message
    status_code = 200
    message = "Done streaming"
    return status_code, message


def start_multiprocess_stream(KAFKA_BROKER_URL, topic, part_id, workstation_id, camera_id):
    try:
        producer_ws = Producer(KAFKA_BROKER_URL, topic)
    except:
        message = "Producer object creation failed"
        status_code = 415
        return message, status_code

    # # Streaming the frames
    logging.info('Initiating the stream')
    status_code = producer_ws.stream_video(part_id, workstation_id, camera_id)
    logging.info('Done streaming')
    if status_code == 200:
        return 1
    else:
        return 0


