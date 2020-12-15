import cv2
import redis
import json
from utils import RedisKeyBuilderWorkstation,CacheHelper

import sys
sys.path.insert(0,"../livis/")
from settings import REDIS_CLIENT_HOST
from settings import REDIS_CLIENT_PORT
import threading
import datetime
from setting_keys import *
import numpy as  np


def camera_initialize(camera_index):
    # cap = cv2.VideoCapture(int(camera_index))
    cap = cv2.VideoCapture(camera_index)
    #cap.set(cv2.CAP_PROP_AUTOFOCUS,0)
    #cap.set(cv2.CAP_PROP_FOCUS,int(40))
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
    return cap



cam_t0 = datetime.datetime.now() 

data = RedisKeyBuilderWorkstation().workstation_info

#Calling redis module
rch = CacheHelper()

cam_list = []
key_list = []
cap_list = []

for cam in data['camera_config']['cameras']:
    camera_index = cam['camera_id']
    camera_name = cam['camera_name']
    key = RedisKeyBuilderWorkstation().get_key(cam['camera_id'],original_frame_keyholder) #WS-01_0_original-frame
    cap = camera_initialize(camera_index = camera_index)
    cap_list.append(cap)
    exec(f'{camera_name} = cap')
    cam_list.append(cam['camera_name'])
    key_list.append(key)


cam_t1 = datetime.datetime.now() 
print('Time taken for initiallizing camera :{} secs'.format((cam_t1-cam_t0).total_seconds()))


failed_count = 0


while True:
    for cap, key in zip(cap_list, key_list):
        ret, frame = cap.read()
        frame_orig = frame.copy()
        
        #if key contains then change it in realtime and set the json 
        try:
            policy = rch.get_json("policy")

            contrast = int(policy['contrast'])
            brightness = int(policy['brightness'])
            saturation = int(policy['saturation'])
            hue = int(policy['hue'])
            exposure = int(policy['exposure'])
            gain = int(policy['gain'])
            mono = policy['mono']
            thresh = int(policy['thresh'])    

            cap.set(cv2.CAP_PROP_CONTRAST,contrast)
            cap.set(cv2.CAP_PROP_BRIGHTNESS,brightness)
            cap.set(cv2.CAP_PROP_SATURATION,saturation)
            cap.set(cv2.CAP_PROP_HUE,hue)
            cap.set(cv2.CAP_PROP_EXPOSURE,exposure)
            cap.set(cv2.CAP_PROP_GAIN,gain)


            if mono == "True":
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            if thresh>=0:
                if len(frame.shape)<=2:
                    #gray
                    pass
                else:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    
                ret,thr = cv2.threshold(frame, thresh, 255, cv2.THRESH_BINARY)
                frame = thr.copy()


        except Exception as  e:
            print(e)
            #print("no policy")
            pass

        rch.set_json({key:frame})
        frame1  = rch.get_json(key)
        
        frame1 = cv2.resize(frame1,(1280,700))
        cv2.imshow("Input_frame",frame1)

    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
  
cv2.destroyAllWindows() 

