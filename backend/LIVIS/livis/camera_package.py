import cv2
from kafka import KafkaProducer
import sys
import json
import base64
from camera_settings import *


class CameraSelect(Camera):
    def __init__(self, KAFKA_BROKER_URL, topic, camera_id):
        self.tfms = {}
        self.KAFKA_BROKER_URL = KAFKA_BROKER_URL
        self.topic = topic
        self.cam_id = camera_id
        self.frame = None
        self.part_id = None
        self.killed = False
        self.thread = None
        self.producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER_URL,
                             value_serializer=lambda value: json.dumps(value).encode(), )
        self.th = None
        self.poll_for_part_id()


        if str(camera_id).find(".") == -1:
            self.cap = cv2.VideoCapture(int(self.cam_id))
            self.is_ip = False
        else:
            self.cap = IPWEBCAM(root_url=str(self.cam_id))
            self.is_ip = True
            print("mobile found")

    def publish_frame_to_kafka(self):
        f_name = str(self.cam_id) + "_tmp.jpg"
        cv2.imwrite(f_name, self.frame)
        with open(f_name, 'rb') as f:
            im_b64 = base64.b64encode(f.read())
        payload_video_frame = {"frame": str(im_b64),"idx":str(self.cam_id)}
        future = self.producer.send(self.topic, value=payload_video_frame)
        report = future.get()


ws_location = sys.argv[1]
cam_ind = []

for i in range(10):
    try:
        cap = cv2.VideoCapture(i)
        ret,frame = cap.read()
        cv2.imwrite(str(i)+'.jpg',frame)
        print('Port :', str(i),' is connected!!')
        cam_ind.append(str(i))
    except:
        pass

### update camera indices to mongo on restart
mp = MongoHelper().getCollection(WORKSTATION_COLLECTION)
coll = mp.find_one({"workstation_location": str(ws_location)})
coll["restart"] = True
coll["available_indexs"] = str(cam_ind)
mp.update({'_id' : coll['_id']}, {'$set' :  coll})


producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER_URL, value_serializer=lambda value: json.dumps(value).encode(), )
topic = str(ws_location)
print("\ntopic "+topic)
print("\ncamera index is "+str(cam_ind))

for i in cam_ind:
    cc = CameraSelect(KAFKA_BROKER_URL, topic, i)
    cc.start()



