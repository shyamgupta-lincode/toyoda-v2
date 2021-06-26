import pyzbar.pyzbar as pyzbar
from common_utils import *
from setting_keys import *
#from LIVIS.livis.toyoda.utils import *
#from LIVIS.livis.parts.utils import *
from common_utils import CacheHelper
import cv2
from memory_profiler import profile
import cProfile
import gc

#kafka 
from kafka import KafkaConsumer

from kafka_utils import Subscriber,imDecoder,imEncoder

rch = CacheHelper()

# mp = MongoHelper().getCollection('inspection_data')
# pr = mp.find_one()
# wid = pr['workstation_id']


# wid = json.load(open("workstation_id.json"))
wid = json.load(open(WORKSTATION_ID_PATH))
@profile
def kanban_reading():
    data2 = RedisKeyBuilderServer(wid).workstation_info
    start_process_object = {}
    # print("---data: ",data2)
    kanban_placed = False
    c = 0
    camera_index = 0
    for cam in data2['cameras']:
        camera_name = cam['camera_name']
        if camera_name == "kanban":
            camera_index = cam['camera_id']


    short_number= None
    detector = cv2.QRCodeDetector()
    count_qr_removed = 0
    process_id = ""
    gc_counter = 0
    while True:
        # i += 1
        # try:
        key = RedisKeyBuilderServer(wid).get_key(camera_index,original_frame_keyholder)
        # print(key)
        kafka_key = key + "_" + "kanban"
        # print("key::::::::::", kafka_key)
        # frame_ = rch.get_json(key)

        sub1 = Subscriber(subscriber_broker_url="localhost:9092",subscriber_topic=kafka_key)

        kafka_data = sub1.get_data()
        frame = imDecoder(kafka_data["frame"])
        # cv2.imshow("frame_kanban",cv2.resize(frame, (324, 240)))
        # cv2.imwrite("kanban_temp.jpg", cv2.resize(frame, (640, 480)))



        data, bbox, _ = detector.detectAndDecode(frame)
        
        if bool(data):
            # try:
            c = 0
            if not kanban_placed:
                part_number = str(data[:-5])
                part_number = part_number.replace("-","")
                short_number = str(data[-4:])
                # print("kanban_data>>>", short_number)
                #print("part_number>>>", part_number)
                rch.set_json({RedisKeyBuilderServer(wid).get_key(camera_index,short_number_keyholder):short_number})
                rch.set_json({RedisKeyBuilderServer(wid).get_key(camera_index,part_number_keyholder):part_number})
                # print(rch.get_json(RedisKeyBuilderServer(wid).get_key(camera_index,short_number_keyholder)))
                # print(rch.get_json(RedisKeyBuilderServer(wid).get_key(camera_index,part_number_keyholder)))
                kanban_placed = True

            else:
                # rch.set_json({RedisKeyBuilderServer(wid).get_key(camera_index,short_number_keyholder):None})
                # rch.set_json({RedisKeyBuilderServer(wid).get_key(camera_index,part_number_keyholder):None}) 
                # print("here..........")
                pass   
                #kanban_placed = False
            c+=1

            # except Exception as e:
            #     print(e)
            #     pass          
        else:
            
            count_qr_removed +=1
            # print("QR removed")
            # print(count_qr_removed)
            if count_qr_removed > 10:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
                rch.set_json({RedisKeyBuilderServer(wid).get_key(camera_index,short_number_keyholder):None})
                rch.set_json({RedisKeyBuilderServer(wid).get_key(camera_index,part_number_keyholder):None})
                kanban_placed = False
                count_qr_removed = 0                                                                                                
            # except Exception as e:
            #     print(e)
            #     pass


        
        #starting the process when the Kanban is placed
        if kanban_placed and c == 1:
            data1 = get_partInfo(short_number)
            # print("data1:::::::",data1)
            workstation_id = data2['_id']
            # print("workstation_id::::::::",workstation_id)
            resp = get_toyoda_running_process(workstation_id)
            if bool(resp):
                # print("Process is already running  1!!!!")
                process_id = str(resp['_id'])
                mp = MongoHelper().getCollection('inspection_data')
                pr = mp.find_one({"_id" : ObjectId(process_id)})
                pr['status'] = 'started'
                mp.update({'_id' : pr['_id']}, {'$set' : pr})
                #print("process id:::::",process_id,"::::",type(process_id))
            else:
                cc = CacheHelper()

                # why to be found out from where the key is getting apended user_id_keyholder
                temp = RedisKeyBuilderServer(workstation_id).get_key(0,user_id_keyholder)
                # print("temp object is ====",temp)
                user_id = cc.get_json(RedisKeyBuilderServer(workstation_id).get_key(0,user_id_keyholder)) 
                # user_id = "9aaedc35-47d2-4b94-bf90-25edf27bc4d8"
                # print(workstation_id)
                # print('user_id:::::::::',user_id)
                obj_dict = {
                    'current_production_count' : data1['planned_production'],
                    'model_number' : data1['model_number'],
                    'part_description' : data1['part_description'],
                    'part_number' : data1['part_number'],
                    'short_number' : data1['short_number'],
                    'user_id' : user_id,
                    'workstation_id' : workstation_id
                }
                # print("obj_dict>>>>>>>>>>>", obj_dict)
                start_process_object = start_toyoda_process(obj_dict)
                #print("start_process_object:",)
                process_id = str(start_process_object['_id'])
                # print("process_id::::::::::", process_id)
                # print("<<<<< ......Process STARTED...... >>>>>")    
                
        # Ending the process when the Kanban is Removed
        elif not kanban_placed and not c == 0:
            workstation_id = data2['_id']
            resp = get_toyoda_running_process(workstation_id)
            if bool(resp):
                # print("Process is already running 2!!!!")
                process_id = str(resp['_id'])
                #print("process id:::::",process_id,"::::",type(process_id))

                #change in logic 
                mp = MongoHelper().getCollection('inspection_data')
                _id = process_id
                print("nspection id is  =======",_id)
                # pr = mp.find_one({"_id" : ObjectId(_id)})
                # pr['manual_inspection_result'] = []
                # mp.update({'_id' : pr['_id']}, {'$set' : pr})
                end_process_object = end_toyoda_process(process_id)
                if end_process_object['status'] == 'completed':
                    c = 0
                    print("<<<<< ......Process ENDED...... >>>>>")
                else:
                    c = 2
                    print("<<<<< ......Process cannot be ENDED...... >>>>>")
                    pass
        else:
            # print("c::::::::::::::", c)
            c=2
            # print("here!!!!!!!!!!!!!!!!!!")
            pass
        if gc_counter % 1000 == 0:
            gc.collect()

        gc_counter += 1                
        # except Exception as e:
        #     print(str(e))
        #     pass    

        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break

cv2.destroyAllWindows()

if __name__ == "__main__": 
    kanban_reading()
