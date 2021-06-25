import cv2
import redis
import json
from common_utils import *
from setting_keys import *
import threading
import datetime
import gc


def camera_initialize(camera_index):
    cap = cv2.VideoCapture(int(camera_index), cv2.CAP_DSHOW)
    #cap = cv2.VideoCapture(camera_index)
    #cap.set(cv2.CAP_PROP_AUTOFOCUS,0)
    # cap.set(cv2.CAP_PROP_FOCUS,int(40))
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    return cap



cam_t0 = datetime.datetime.now() 
wid = json.load(open("workstation_id.json"))
data = RedisKeyBuilderServer(wid).workstation_info
print("data..............>>>", data)

#Calling redis module
rch = CacheHelper()

cam_list = []
key_list = []
cap_list = []


for cam in data['cameras']:
    try:
        camera_index = int(cam['camera_id'])
    except:
        camera_index = cam['camera_id']

    camera_name = cam['camera_name']
    #print("camera_name........",camera_name)
    key = RedisKeyBuilderServer(wid).get_key(cam['camera_id'],original_frame_keyholder) #WS-01_0_original-frame
    cap = camera_initialize(camera_index = camera_index)
    cap_list.append(cap)
    cam_list.append(cam['camera_name'])
    key_list.append(key)

cam_t1 = datetime.datetime.now()
print("key list...........", key_list)
print("cap list..........", cap_list)


gc_counter = 0
while True:
    try:
        for cap, key in zip(cap_list, key_list):
            ret, frame = cap.read()
            rch.set_json({key:frame})
            print(key)
            # cv2.imshow("frame",frame)
            del frame
            del key
            if gc_counter % 1000 == 0:
                collected = gc.collect()
                print("GC Collected>>>>>>>>", collected)
            gc_counter+=1
            # print(gc_counter)

    except Exception as e:
        print(str(e))
        pass

    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
  
cv2.destroyAllWindows() 
