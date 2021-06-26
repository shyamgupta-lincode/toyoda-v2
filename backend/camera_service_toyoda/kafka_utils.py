import cv2
import json
import base64
from kafka import KafkaProducer, KafkaConsumer
import numpy as np
from bson import ObjectId
import os 


class Publisher: 

    def __init__(self,publisher_broker_url,publisher_topic):

        self.publisher_broker_url = publisher_broker_url
        self.publisher_topic = publisher_topic
        self.producer = KafkaProducer(bootstrap_servers=[self.publisher_broker_url])

    def send_data(self,data):
        
        try:
            serialized_data = json.dumps(data).encode("utf-8")
            self.producer.send(self.publisher_topic,serialized_data)
        except Exception as e:
            print("Exception Encountered")
            print(e)


class Subscriber:

    def __init__(self,subscriber_broker_url,subscriber_topic):

        self.subscriber_broker_url = subscriber_broker_url
        self.subscriber_topic = subscriber_topic
        self.consumer = KafkaConsumer(bootstrap_servers=[self.subscriber_broker_url])
        self.consumer.subscribe(topics=[self.subscriber_topic])

    def get_data(self):

        try:
            print("Fetching Data")
            serialized_data = next(self.consumer).value.decode("utf-8")
            data = json.loads(serialized_data)
            return data

        except Exception as e:
            print("Exception Encountered")
            print(e)

            
def imDecoder(img_str):
    
    im_b64 = bytes(img_str[2:], 'utf-8')
    im_binary = base64.b64decode(im_b64)
    im_arr = np.frombuffer(im_binary, dtype=np.uint8)
    frame = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
    
    return frame

def imEncoder(image):
    img = str(ObjectId()) + ".jpg"
    cv2.imwrite(img,image)
    with open(img, 'rb') as f:
        im_b64 = base64.b64encode(f.read())
    os.remove(img)
    return str(im_b64)
