import pyzbar.pyzbar as pyzbar
from common_utils import *
from setting_keys import *
#from LIVIS.livis.toyoda.utils import *
#from LIVIS.livis.parts.utils import *
from common_utils import CacheHelper
import cv2

rch = CacheHelper()



#qr_detector = cv2.QRCodeDetector()

# def read_qr(qr_detector , frame):
#     data, bbox, _ = detector.detectAndDecode(frame)
#     if bool(bbox):
#         #string manipulation
#         short_number = 
#         part_number = 
#         return short_number , part_number
#     else:
#         return None ,None


mp = MongoHelper().getCollection('inspection_data')
pr = mp.find_one()
wid = pr['workstation_id']


def kanban_reading():

    data2 = RedisKeyBuilderServer(wid).workstation_info
    start_process_object = {}
    #print("---data: ",data)
    kanban_placed = False
    c = 0
    camera_index = 0
    for cam in data2['cameras']:
        camera_name = cam['camera_name']
        if camera_name == "kanban":
            camera_index = int(cam['camera_id'])

    
    #if cam['camera_name'] == 'kanban':
        #kanban_camera_index = cam['camera_id']

    short_number= None
    detector = cv2.QRCodeDetector()
    count_qr_removed = 0
    process_id = ""

    while True:
        try:
            key = RedisKeyBuilderServer(wid).get_key(camera_index,original_frame_keyholder)
            #print("key::::::::::", key)
            frame = rch.get_json(key)
            #print("------frame; ",frame)
            # frame = cv2.resize(frame,(640,480))
            # cv2.imshow("kanban..........",frame)

            #decodedObjects = pyzbar.decode(frame)
            
            # try:
            data, bbox, _ = detector.detectAndDecode(frame)
            #print("------data; ",data)
            # except:
                # print("bad frame")
                #print(rch.get_json(RedisKeyBuilderServer(wid).get_key(cam['camera_id'],short_number_keyholder)))
            
            if bool(data):
                try:
                    c = 0
                    if not kanban_placed:
                        # try:
                        # display the image with lines
                        #print("[+] QR Code detected, data:", data)
                        # for obj in decodedObjects:
                        part_number = str(data[:-5])
                        part_number = part_number.replace("-","")
                        short_number = str(data[-4:])
                        #print("kanban_data>>>", short_number)
                        #print("part_number>>>", part_number)
                        rch.set_json({RedisKeyBuilderServer(wid).get_key(camera_index,short_number_keyholder):short_number})
                        rch.set_json({RedisKeyBuilderServer(wid).get_key(camera_index,part_number_keyholder):part_number})


                        # print(rch.get_json(RedisKeyBuilderServer(wid).get_key(camera_index,short_number_keyholder)))
                        # print(rch.get_json(RedisKeyBuilderServer(wid).get_key(camera_index,part_number_keyholder)))
                        kanban_placed = True

                    else:
                        # rch.set_json({RedisKeyBuilderServer(wid).get_key(camera_index,short_number_keyholder):None})
                        # rch.set_json({RedisKeyBuilderServer(wid).get_key(camera_index,part_number_keyholder):None}) 
                        print("here..........")
                        pass   
                        #kanban_placed = False

                        # except Exception as e:
                        #     # print(e)
                        #     pass
                    c+=1
                except Exception as e:
                    print(e)
                    pass          
            else:
                try:
                    count_qr_removed +=1
                    print("QR removed")
                    print(count_qr_removed)
                    if count_qr_removed > 10:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
                        rch.set_json({RedisKeyBuilderServer(wid).get_key(camera_index,short_number_keyholder):None})
                        rch.set_json({RedisKeyBuilderServer(wid).get_key(camera_index,part_number_keyholder):None})
                        kanban_placed = False
                        count_qr_removed = 0                                                                                                
                except Exception as e:
                    print(e)
                    pass


            
            #starting the process when the Kanban is placed
            # print("------short_num; ",short_number)
            if kanban_placed and c == 1:
                data1 = get_partInfo(short_number)
                print("data1:::::::",data1)
                #user_id = "6ff49cf5-f25c-486d-8db0-912b104d36dd"
                workstation_id = data2['_id']
                print("workstation_id::::::::",workstation_id)
                resp = get_toyoda_running_process(workstation_id)
                if bool(resp):
                    print("Process is already running  1!!!!")
                    process_id = str(resp['_id'])
                    mp = MongoHelper().getCollection('inspection_data')
                    pr = mp.find_one({"_id" : ObjectId(process_id)})
                    pr['status'] = 'started'
                    mp.update({'_id' : pr['_id']}, {'$set' : pr})
                    #print("process id:::::",process_id,"::::",type(process_id))
                else:
                    cc = CacheHelper()
                    user_id = cc.get_json(RedisKeyBuilderServer(workstation_id).get_key(0,user_id_keyholder)) 
                    print('user_id:::::::::',user_id)
                    obj_dict = {
                        'current_production_count' : data1['planned_production'],
                        'model_number' : data1['model_number'],
                        'part_description' : data1['part_description'],
                        'part_number' : data1['part_number'],
                        'short_number' : data1['short_number'],
                        'user_id' : user_id,
                        'workstation_id' : workstation_id
                    }
                    start_process_object = start_toyoda_process(obj_dict)
                    #print("start_process_object:",)
                    process_id = str(start_process_object['_id'])
                    print("process_id::::::::::", process_id)
                    print("<<<<< ......Process STARTED...... >>>>>")    
                    
            # Ending the process when the Kanban is Removed
            elif not kanban_placed and not c == 0:
                workstation_id = data2['_id']
                resp = get_toyoda_running_process(workstation_id)
                if bool(resp):
                    print("Process is already running 2!!!!")
                    process_id = str(resp['_id'])
                    #print("process id:::::",process_id,"::::",type(process_id))
                    end_process_object = end_toyoda_process(process_id)
                    if end_process_object['status'] == 'completed':
                        c = 0
                        print("<<<<< ......Process ENDED...... >>>>>")
                    else:
                        c = 2
                        print("<<<<< ......Process cannot be ENDED...... >>>>>")
                        pass
            else:
                print("c::::::::::::::", c)
                c=2
                print("here!!!!!!!!!!!!!!!!!!")
                pass

        except Exception as e:
            print(str(e))
            pass    

        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break

cv2.destroyAllWindows()


kanban_reading()
