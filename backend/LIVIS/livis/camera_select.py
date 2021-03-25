import cv2
from kafka import KafkaProducer
from livis.settings import *
import sys
import json
import base64
#from camera_service import *

ws_id = sys.argv[1]
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

str_ = ""
payload = {}
for i in cam_ind:
    str_ = str_ + i + "_"
    cap = cv2.VideoCapture(int(i))
    ret, frame = cap.read()
    f_name = str(i) + "_cstmp.jpg"
    cv2.imwrite(f_name, frame)
    with open(f_name, 'rb') as f:
        im_b64 = base64.b64encode(f.read())
    payload[str(i)] = str(im_b64)

producer1 = KafkaProducer(bootstrap_servers=KAFKA_BROKER_URL, value_serializer=lambda value: json.dumps(value).encode(), )
topic1 = ws_id+"_camera_indexes"


while True:
    producer1.send(topic1, value = payload)


