import cv2
import redis
import json
from common_utils import *
from setting_keys import *
import threading
import datetime


def camera_initialize(camera_index):
    # cap = cv2.VideoCapture(int(camera_index))
    cap = cv2.VideoCapture(camera_index)
    #cap.set(cv2.CAP_PROP_AUTOFOCUS,0)
    # cap.set(cv2.CAP_PROP_FOCUS,int(40))
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    return cap



cam_t0 = datetime.datetime.now() 
wid = json.load(open("workstation_id.json"))
print("wid......", wid)
data = RedisKeyBuilderServer(wid).workstation_info

#Calling redis module
rch = CacheHelper()

cam_list = []
key_list = []
cap_list = []

print("data of camera....", data)
for cam in data['cameras']:
    try:
        camera_index = int(cam['camera_id'])
    except:
        camera_index = cam['camera_id']
    print("camera_index.......",camera_index)
    camera_name = cam['camera_name']
    print("camera_name........",camera_name)
    key = RedisKeyBuilderServer(wid).get_key(cam['camera_id'],original_frame_keyholder) #WS-01_0_original-frame
    cap = camera_initialize(camera_index = camera_index)
    cap_list.append(cap)
    print("camera_index........", camera_index, type(camera_index))
    exec(f'{camera_name} = cap')
    cam_list.append(cam['camera_name'])
    key_list.append(key)

cam_t1 = datetime.datetime.now() 
print('Time taken for initiallizing camera :{} secs'.format((cam_t1-cam_t0).total_seconds()))


#img = cv2.imread('felt.jpg')
# cap_1 = cv2.VideoCapture(1)#("Pillar part with SRS CLip Absenece(LH).mp4")

#cap_1.set(2,1800)

cap_dict = {}
failed_count = 0
cc = 0
while True:
    try:
        for cap, key in zip(cap_list, key_list):
            print("KEYEYEYEYEYEY : : : " , key)
            if "mp4" not in key:
                ret, frame = cap.read()
                print("Here  0....!!!!!")
                # cv2.imshow("First Frame...............",frame)
                #print(frame.shape)
                #print("reading from KANBAN Camera!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            else:
                if cap_dict:
                    ret, frame = cap_dict[cc].read()
                    print("Here  1....!!!!!")
                else:
                    cap_dict[cc] = camera_initialize(camera_index=camera_index)
                    ret, frame = cap_dict[cc].read()
                    print("Here  2....!!!!!")
                try:
                    frame.shape
                except:
                    if cap_dict:
                        cap_dict.pop(cc)
                    cap_dict[cc] = camera_initialize(camera_index=camera_index)
                    print("Here  3....!!!!!")

            # ret, frame = cap_1.read()
            #frame = img
            #print(frame.shape)
            # try:
            print(key)
            rch.set_json({key:frame})
            print("wrote a frame to redis! ::::::::::", key)
        
            frame1  = rch.get_json(key)
            #print(frame1.shape)
            #frame1 = cv2.resize(frame1,(1280,700))
            # cv2.imshow(key,frame1)
            
    except Exception as e:
                print(str(e))
                pass



    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
  
cv2.destroyAllWindows() 
