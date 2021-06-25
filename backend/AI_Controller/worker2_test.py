from detector_module import *
from common_utils import CacheHelper,MongoHelper
from setting_keys import *
from model_settings import *
import datetime
from kanban import static_kanban
from qrcode_generator import *
from common_utils import *
import time
import random
import gc

import datetime
# from flask import Flask, Response
from kafka import KafkaConsumer

from kafka_utils import Subscriber,imDecoder,imEncoder

rch = CacheHelper()
# wid = json.load(open("workstation_id_ws2.json"))
wid = json.load(open(WORKSTATION_ID2_PATH))

def set_mongo_payload(predicted_taco, defects_list, taco_fail ,short_number, part_counter, camera_index, frame, frame1):
    cname =  rch.get_json(RedisKeyBuilderServer(wid).get_key(0,current_inspection_id_keyholder))
    mh = MongoHelper().getCollection(cname)
    # taco_fail = taco_fail
    # print('inside set mongo pyload:',camera_index)
    # print("rescan_value : ",rch.get_json(RedisKeyBuilderServer(wid).get_key(camera_index,rescan_keyholder)))
    # print('key: ', RedisKeyBuilderServer(wid).get_key(camera_index,rescan_keyholder))
    original_image = frame
    predicted_image = frame1

    taco_pass, features_list, accepted, taco_fail  =  match_kanban(predicted_taco,short_number, taco_fail)
    # print("taco_fail>>>>>>>>", taco_fail)
    # print("taco_pass>>>>>>>>", taco_pass)
    # print("features_list>>>>", features_list)
    # print("defects_list>>>>>", defects_list)
    # print("isAccepted status", accepted)

    date_time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    # date_time = datetime.now()
    # print("date_time:::::",date_time)
    upd_obj={}
    upd_obj['short_number'] = short_number
    #upd_obj['serial_number'] = part_counter
    upd_obj['feature_list'] = features_list#predicted_taco['feature_list']
    upd_obj['defect_list'] = defects_list#predicted_taco['defect_list']
    upd_obj['taco_fail'] = taco_fail
    upd_obj['taco_pass'] = taco_pass
    upd_obj['isAccepted'] = accepted
    upd_obj['timestamp'] = date_time
    upd_obj['qr_string'] = ""
    # print("rescan: ",rch.get_json(RedisKeyBuilderWorkstation().get_key(camera_index,rescan_keyholder)))
    #print("updated_object",upd_obj)

    if accepted :
        part_counter = mh.find({'isAccepted' : True}).count()
        # upd_obj['serial_number'] = part_counter + 1
        qr_string = qrcode_generator(short_number, part_counter)
        upd_obj['qr_string'] = "data:image/png;base64,"+qr_string

        rch.set_json({RedisKeyBuilderServer(wid).get_key(0,part_accepted_keyholder) : True})
        rch.set_json({RedisKeyBuilderServer(wid).get_key(0,process_completed) : True})  
        rch.set_json({RedisKeyBuilderServer(wid).get_key(0,qr_string_keyholder) : qr_string})

    else:
        rch.set_json({RedisKeyBuilderServer(wid).get_key(0,qr_string_keyholder) : ""})  

   
    if rch.get_json(RedisKeyBuilderServer(wid).get_key(camera_index,rescan_keyholder)):#Rescan
        #update the DB
        myquery = { "_id": ObjectId(rch.get_json(RedisKeyBuilderServer(wid).get_key(camera_index,last_entry_id_keyholder))) }
        newvalues = { "$set" : upd_obj }
        #mycol.update_one(, newvalues)
        # rch.set_json({RedisKeyBuilderWorkstation().get_key(cam['camera_id'],rescan_keyholder) : entry_id.inserted_id})
        rch.set_json({RedisKeyBuilderServer(wid).get_key(camera_index,rescan_keyholder) : False})
        mh.update(myquery, newvalues)
        # print('updating Rescan!!!!!!!!!!!!!!!')

    elif rch.get_json(RedisKeyBuilderServer(wid).get_key(camera_index,rescan_keyholder)) == False:
        if (bool(taco_fail) is True) & (bool(defects_list) is False):
            #part_counter += 1
            #part_counter = mh.find().count()
            #upd_obj['serial_number'] = part_counter + 1
            #print("upd_obj::::::::::",upd_obj)
            ##setting the rescan flag as True
            production_count = rch.get_json(RedisKeyBuilderServer(wid).get_key(0,production_count_keyholder))
            if int(production_count) > int(part_counter):
                rch.set_json({RedisKeyBuilderServer(wid).get_key(camera_index,rescan_keyholder) : True})
                entry_id = mh.insert(upd_obj)
                # print('rescan_inserting!!!!!!!!!!!!!!!!!!!!')
                rch.set_json({RedisKeyBuilderServer(wid).get_key(camera_index,last_entry_id_keyholder) : entry_id})
                """#save images
                unique_id = entry_id.inserted_id
                actual_img_path = save_actual(original_image  ,shot_number =short_number , unique_id = unique_id)
                predicted_img_path = save_predicted(predicted_image  ,shot_number = short_number, unique_id = unique_id)
                print(actual_img_path , predicted_img_path)"""
                
        else:
            rch.set_json({RedisKeyBuilderServer(wid).get_key(camera_index,rescan_keyholder) : False})
            #part_counter += 1 
            part_counter = mh.find({'isAccepted' : True}).count()
            # print("upd_obj  1111::::::::::",upd_obj)
            production_count = rch.get_json(RedisKeyBuilderServer(wid).get_key(0,production_count_keyholder))
            # print("part_counter::::::::::",part_counter)
            # print("production_count::::::::::",production_count)
            #print("serial_number::::::::::",upd_obj['serial_number'])
            if int(production_count) > int(part_counter):
                #print("production_count::::::::::",production_count)
                upd_obj['serial_number'] = part_counter + 1
                entry_id = mh.insert(upd_obj)
                # print('inserting!!!!!!!!!!!!!!!!!!!!')
                rch.set_json({RedisKeyBuilderServer(wid).get_key(camera_index,last_entry_id_keyholder) : entry_id})
                
                """#save images
                unique_id = entry_id.inserted_id
                actual_img_path = save_actual(original_image  ,shot_number =short_number , unique_id = unique_id)
                predicted_img_path = save_predicted(predicted_image  ,shot_number = short_number, unique_id = unique_id)
                print(actual_img_path , predicted_img_path)"""
            
            else :
                pass
            
    return part_counter


def match_kanban(predicted_taco,short_number,taco_fail):

    ## if predicted_taco is same as kanban : 
    # taco_fail = {}
    taco_pass = {}
    features_list = []
    # defects_list = []
    #print('static_kanban:')
    #print((static_kanban[str(short_number)]['feature_list']))
    #print('predicted_taco')
    #print(predicted_taco)
    
    # if len(predicted_taco) >= len(static_kanban[str(short_number)]['feature_list']):
    for  d in static_kanban[str(short_number)]['feature_list']:

        # print("d main>>>>", d)
        # class_name = static_kanban['IG95']['feature_list'][d] 
        """if d in predicted_taco:
            # print('d' , d)
            fn , cnt = list(d.values())
            if fn != 'Shot_Shot_Absence': 
                features_list.append(fn)
                taco_pass.update({fn : cnt})
        else:
            # print("d>>>>", d)
            fn , cnt = list(d.values()) 
            if (fn == 'Shot_Shot_Absence'):
                defects_list.append("Shot_Shot_Presence")
                taco_fail.update({"Shot_Shot_Presence":cnt})

            else:        
                taco_fail.update({fn : cnt})"""

        if d in predicted_taco:
            fn, cnt = list(d.values())
            features_list.append(fn)
            taco_pass.update({fn : cnt})
        else:
            fn, cnt = list(d.values())
            # if (fn != "Part_Presence") and (fn != "Felt_Presence") and (fn != "Clip_Presence") and (fn != "Black_Clip_Presence"): #and (fn != "Shot_Shot_Absence"):
            taco_fail.update({fn : cnt})
        # else:
        #     try:
        #         fn, cnt = list(d.values())
        #         taco_fail.update({fn : cnt})

        #     except:
        #         pass

        #     fn, cnt = list(d.values())
        #     if fn != 'Shot_Shot_Absence':
        #         taco_fail.update({fn : cnt})
                         

    if bool(taco_fail):
        accepted = False
    else:
        accepted = True

    return taco_pass, features_list, accepted, taco_fail 


def worker():
    requested_models = {}
    #mp = MongoHelper().getCollection('inspection_data')
    #pr = mp.find_one()
    #wid = pr['workstation_id']

    # workstation_id = "Dummy"
    camera_index_side = None
    # workstation_id = "WS-02_test.mp4_original-frame"
    # key = RedisKeyBuilderServer(wid).get_key(cam['camera_id'],original_frame_keyholder)
    # sub1 = Subscriber(subscriber_broker_url="localhost:9092",subscriber_topic=workstation_id+"_kanban")
    # sub2 = Subscriber(subscriber_broker_url="localhost:9092",subscriber_topic=workstation_id+"_top")
    # sub3 = Subscriber(subscriber_broker_url="localhost:9092",subscriber_topic=workstation_id+"_side")
    

    data = RedisKeyBuilderServer(wid).workstation_info
    part_counter = 0
    part_presence = False
    models_loaded = False
    # print("Data::::",data)
    #Initialling the rescan False
    for cam in data['cameras']:
        # camera_index = cam['camera_id']
        # camera_name = cam['camera_name']
        # print("Data in for       :",data)
        if cam['camera_name'] == 'top':
            camera_index = cam['camera_id']
            key = RedisKeyBuilderServer(wid).get_key(cam['camera_id'],original_frame_keyholder)
            sub2 = Subscriber(subscriber_broker_url="localhost:9092",subscriber_topic=key+"_"+cam['camera_name'])

        if cam['camera_name'] == 'side':
            camera_index_side = cam['camera_id']
            key = RedisKeyBuilderServer(wid).get_key(cam['camera_id'],original_frame_keyholder)
            sub3 = Subscriber(subscriber_broker_url="localhost:9092",subscriber_topic=key+"_"+cam['camera_name'])

        if cam['camera_name'] == 'kanban':
            kanban_camera_index = cam['camera_id']
            key = RedisKeyBuilderServer(wid).get_key(cam['camera_id'],original_frame_keyholder)
            sub1 = Subscriber(subscriber_broker_url="localhost:9092",subscriber_topic=key+"_"+cam['camera_name'])

        

    rch.set_json({RedisKeyBuilderServer(wid).get_key(camera_index,rescan_keyholder) : False})
    if bool(camera_index_side):
        rch.set_json({RedisKeyBuilderServer(wid).get_key(camera_index_side,rescan_keyholder) : False})
    # print("rescan_value : ",rch.get_json(RedisKeyBuilderServer(wid).get_key(camera_index,rescan_keyholder)))
    # print('key: ', RedisKeyBuilderServer(wid).get_key(camera_index,rescan_keyholder))
    # print("checking first camera index>>>>>>>>>", camera_index )
    model_1 = Pillar_part_presence_abs()    

    ii = 0
    short_number = None
    prediction_frame_done = 0
    # cap_tmp = cv2.VideoCapture("/home/gokul/Desktop/Toyoda/utilsandmodels/101.mp4")
    tin = time.time()
    while True:
        try:
        
            curr_inspection_id = rch.get_json(RedisKeyBuilderServer(wid).get_key(0,current_inspection_id_keyholder)) 
            key1 = RedisKeyBuilderServer(wid).get_key(camera_index,predicted_frame_keyholder)
            data1 = RedisKeyBuilderServer(wid).workstation_info
            #setting the frame to reddis

            cr = MongoHelper().getCollection('inspection_data')
            insp_obj = cr.find_one({'_id' : ObjectId(curr_inspection_id)})
            # print("Entering while::")

            if insp_obj:
                if insp_obj['is_manual'] == True:
                    print("in Manual Mode!!")
                    short_number = insp_obj["short_number"]
                    part_number = insp_obj["part_number"]
                    # print("short-number:::::::::", short_number)
                    # print("part-number::::::::::", part_number)

                elif insp_obj['is_manual'] == False:
                    print("in Automatic Mode!!")
                    short_number = rch.get_json(RedisKeyBuilderServer(wid).get_key(kanban_camera_index,short_number_keyholder))
                    part_number = rch.get_json(RedisKeyBuilderServer(wid).get_key(kanban_camera_index,part_number_keyholder))
                    # print("testing.........short_number", short_number)
                    # print("testing.........part_number", part_number)

                else:
                    print("No mode is selected")    
                # print('short_number:',short_number)

            # short_number = "IG98"

            ############ Load models ##############
            if bool(short_number):
                # checking if model in Requested_models and clearnig when new model is chose
                if short_number not in requested_models:
                    requested_models.clear()
                    requested_models[short_number] = [i() for i in MODEL_MAP[short_number]]
                print("Requested_models:::::::::::::::",requested_models)
                print("currently running model number::::::", short_number)


                #### Iterate cameras and sent to predictors
                predicted_taco = []

                for cam in data1['cameras']:
                    if cam['camera_name'] == 'top':
                        camera_index1 = cam['camera_id']
                        # print("cam ind:::::",camera_index1)
                    if cam['camera_name'] == 'side':
                        camera_index2 = cam['camera_id']

                #Getting the original frame using original_frame_keyholder and camera_index


                ###   figure out how to fetch key for top and side camera 
                if short_number in TOP_CAMERA_USAGE :
                    camera_index_actual = camera_index1
                    #kafka for pillar camera frame
                    sub = sub2

                elif short_number in SIDE_CAMERA_USAGE:
                    camera_index_actual = camera_index2
                    #kafka for roof camera frame
                    sub = sub3

                # print("Topics:",sub.topics())

                # key = RedisKeyBuilderServer(wid).get_key(camera_index_actual,original_frame_keyholder)
                # print("Key>>>>>to check", key)


                # Write logic to choose proper subscriber based on short number
                # 
                # print("sub  is  =========",sub)
                
                st = time.time()
                # kafka_data = sub.get_data()
                # # print("kafka data is ======",kafka_data)

                # frame = imDecoder(kafka_data["frame"])

                # cv2.imshow("frame1 checkin", cv2.resize(frame, (640, 480)))
                # cv2.imwrite("worker_input.jpg",cv2.resize(frame, (640, 480)))
                # frame = rch.get_json(key)
                # print(frame.shape)
                # exit()

                # cv2.imshow("check", cv2.resize(frame, (640, 480)))
                # print("checking the camera index>>>>>>>>>", camera_index_actual)

                # if prediction_frame_done == 0:
                #     rch.set_json({key1 : frame})

                # part_presence  = random.choice([True,False])
                # print("part_presence:",part_presence)
                #if part_presence is False:
                #shyamdd
                time_tmp = tin - time.time()
                cnty = 0
                if rch.get_json(RedisKeyBuilderServer(wid).get_key(0,process_start_keyholder)):
                    kafka_data = sub.get_data()
                # print("kafka data is ======",kafka_data)

                    frame = imDecoder(kafka_data["frame"])
                    # cv2.imwrite("worker_input.jpg",cv2.resize(frame, (640, 480)))
                    # cv2.imshow("orig frame",cv2.resize(frame, (640,480)))


                # if cnty % 1000 == 0:
                    #Inferencing the Part Presnce and absence model 
                    model_1.inference(frame)
                    frame_failed = False
                    print("model_1.predictions", model_1.predictions)

                    ##Based on the model Inference setting the flag Part_Presence
                    if bool(model_1.predictions): # and not frame_failed:
                        # print("inside-----------------")
                        if model_1.predictions['count'] == 1 and model_1.predictions["feature_name"] == "Part_Presence" :
                            part_presence = True

                        else:
                            part_presence = False
                            ii = 0

                        ###If part_presence flag is true making predictions on the same image for features and defects models.
                        # print("Part_presence>>>>>>", part_presence)
                        if part_presence is True: # and ii == 0: 
                            i = 0
                            frame1 = frame.copy()
                            # print("frame1 shape>>>>>>>>>>>>>>>>>>>>>>",frame1.shape)
                            #frame1 = rch.get_json(RedisKeyBuilderServer(wid).get_key(camera_index,original_frame_keyholder))
                            for model in requested_models[short_number]:
                                print(" >>>>>", model)
                                # st = time.time()

                                ###Inferencing the models and giving predicted_tco, defects_list, taco_fail
                                model.inference(frame)
                                key = RedisKeyBuilderServer(wid).get_key(camera_index_actual,predicted_frame_keyholder)
                                # print("checkin the predicted frame keyholder>>>", key)

                                #setting the frame to reddis
                                # rch.set_json({key : model.predicted_frame})
                                # cc = rch.get_json(key)
                                # cv2.imshow("checkkkkkkkkk", cv2.resize(cc,(640, 480)))

                                ###Getting the results after prediction from detector_module
                                prediction_frame_done = 1
                                predicted_taco = model.predicted_taco
                                defects_list = model.defects_list
                                taco_fail = model.taco_fail
                                # print("predicted_taco::::::::::::", predicted_taco)
                                i += 1

                                ###making the bounding box and labels on the image 
                                (boxes, scores, classes, num) = model.meta 
                                frame1 = vis_util.visualize_boxes_and_labels_on_image_array(
                                                                frame1,
                                                                np.squeeze(boxes),
                                                                np.squeeze(classes).astype(np.int32),
                                                                np.squeeze(scores),
                                                                model.category_index,
                                                                use_normalized_coordinates=True,
                                                                line_thickness=3,
                                                                min_score_thresh = model.min_threshold)

                                # cv2.imshow("Frame last::", cv2.resize(frame1, (640, 480)))

                            ###final frame that will be set as predicted_frame    
                            # rch.set_json({key : frame1})  
                            # use same key and send to kafka 

                            
                            # cdc = rch.get_json(key)
                            # cv2.imshow("frame1 checkin", cv2.resize(frame1, (640, 480)))
                            # cv2.imwrite("worker_output.jpg",cv2.resize(frame1, (640, 480)))
                            
                            part_counter = set_mongo_payload(predicted_taco, defects_list, taco_fail, short_number, part_counter, camera_index_actual, frame, frame1)    
                            # ii+=1
                            # part_presence = False
                            rch.set_json({RedisKeyBuilderServer(wid).get_key(0,process_start_keyholder) : False})
                            # end = time.time() - st
                            # print("end time is     ======",end)
                            del frame1
                            del key
                end = time.time() - st
                print("frame fetching time is ", end)

                # cnty += 1

            else:
                requested_models = {}
                # data = RedisKeyBuilderWorkstation().workstation_info
                part_counter = 0
                part_presence = False
                models_loaded = False            

        except Exception as e:
            print(e)
            pass


        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break

cv2.destroyAllWindows() 

###calling the worker funtion while running the script
worker()     

######KAFKA###
# app = Flask(__name__)

# @app.route('/', methods=['GET'])
# def video():
#     """
#     This is the heart of our video display. Notice we set the mimetype to 
#     multipart/x-mixed-replace. This tells Flask to replace any old images with 
#     new values streaming through the pipeline.
#     """
#     return Response(
#         get_video_stream(), 
#         mimetype='multipart/x-mixed-replace; boundary=frame')

# def get_video_stream():
#     """
#     Here is where we recieve streamed images from the Kafka Server and convert 
#     them to a Flask-readable format.
#     """
#     for msg in consumer:
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpg\r\n\r\n' + msg["frame"].value + b'\r\n\r\n')




# ####


# if __name__ == "__main__":
#     worker()    
#     app.run(host='0.0.0.0', debug=True)


###calling the worker funtion while running the script
