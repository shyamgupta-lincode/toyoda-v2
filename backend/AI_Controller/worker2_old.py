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
    
rch = CacheHelper()
wid = json.load(open("workstation_id_ws2.json"))

def set_mongo_payload(predicted_taco ,short_number, part_counter, camera_index):
    cname =  rch.get_json(RedisKeyBuilderServer(wid).get_key(0,current_inspection_id_keyholder))
    mh = MongoHelper().getCollection(cname)

    # print('inside set mongo pyload:',camera_index)
    # print("rescan_value : ",rch.get_json(RedisKeyBuilderServer(wid).get_key(camera_index,rescan_keyholder)))
    # print('key: ', RedisKeyBuilderServer(wid).get_key(camera_index,rescan_keyholder))

    taco_pass ,taco_fail ,features_list,defects_list, accepted  =  match_kanban(predicted_taco,short_number)
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
            else :
                pass
            
    return part_counter


def match_kanban(predicted_taco,short_number):

    ## if predicted_taco is same as kanban : 
    taco_fail = {}
    taco_pass = {}
    features_list = []
    defects_list = []



    #print('static_kanban:')
    #print((static_kanban[str(short_number)]['feature_list']))
    #print('predicted_taco')
    #print(predicted_taco)
    
    # if len(predicted_taco) >= len(static_kanban[str(short_number)]['feature_list']):
    for  d in static_kanban[str(short_number)]['feature_list']:

        # print("d main>>>>", d)
        # class_name = static_kanban['IG95']['feature_list'][d] 
        if d in predicted_taco:
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
                taco_fail.update({fn : cnt})

    if bool(taco_fail):
        accepted = False
    else:
        accepted = True
    
    print("taco_fail>>>>>>>>", taco_fail)
    print("taco_pass>>>>>>>>", taco_pass)
    print("features_list>>>>", features_list)
    print("defects_list>>>>>", defects_list)
    print("isAccepted status", accepted)

    return taco_pass, taco_fail, features_list, defects_list, accepted 


def worker():
    requested_models = {}
    #mp = MongoHelper().getCollection('inspection_data')
    #pr = mp.find_one()
    #wid = pr['workstation_id']
    data = RedisKeyBuilderServer(wid).workstation_info
    # print("data...........worker", data)
    part_counter = 0
    part_presence = False
    models_loaded = False

    #Initialling the rescan False
    for cam in data['cameras']:
        # camera_index = cam['camera_id']
        # camera_name = cam['camera_name']
        if cam['camera_name'] == 'top':
            camera_index = cam['camera_id']
        if cam['camera_name'] == 'kanban':
            kanban_camera_index = cam['camera_id']

    rch.set_json({RedisKeyBuilderServer(wid).get_key(camera_index,rescan_keyholder) : False})
    # print("rescan_value : ",rch.get_json(RedisKeyBuilderServer(wid).get_key(camera_index,rescan_keyholder)))
    # print('key: ', RedisKeyBuilderServer(wid).get_key(camera_index,rescan_keyholder))

    model_1 = Pillar_part_presence_abs()    

    ii = 0
    short_number = None
    prediction_frame_done = 0
    # cap_tmp = cv2.VideoCapture("/home/gokul/Desktop/Toyoda/utilsandmodels/101.mp4")
    tin = time.time()
    while True:
        try:
            #### Load models
            # short_number = rch.get_json("current_part")
            curr_inspection_id = rch.get_json(RedisKeyBuilderServer(wid).get_key(0,current_inspection_id_keyholder)) 
            key1 = RedisKeyBuilderServer(wid).get_key(camera_index,predicted_frame_keyholder)
            data1 = RedisKeyBuilderServer(wid).workstation_info
            #setting the frame to reddis

            cr = MongoHelper().getCollection('inspection_data')
            insp_obj = cr.find_one({'_id' : ObjectId(curr_inspection_id)})

            if insp_obj:
                if insp_obj['is_manual'] == True:
                    # print("in Manual Mode!!")
                    short_number = insp_obj["short_number"]
                    part_number = insp_obj["part_number"]
                    print("short-number:::::::::", short_number)
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

            ##Loading Models:
            if bool(short_number):
                # if models_loaded is False:
                if short_number not in requested_models:
                    requested_models.clear()
                    requested_models[short_number] = [i() for i in MODEL_MAP[short_number]]

                    # print(short_number)
                    # models_loaded = True
                        # print("hereeeeeeeeeeeeeeeee")

                print("Requested_models:::::::::::::::",requested_models)

                #### Iterate cameras and sent to predictors
                predicted_taco = []

                for cam in data1['cameras']:
                    if cam['camera_name'] == 'top':
                        camera_index1 = cam['camera_id']
                        print("cam ind:::::",camera_index1)
                        # print("cam name:::::",camera_name)


                #     if cam['camera_name'] == 'top_camera':
                key = RedisKeyBuilderServer(wid).get_key(camera_index1,original_frame_keyholder)
                print("KEY: : : : : : : :" , key)
                frame = rch.get_json(key)
                # cv2.imshow("frame", frame)
                
                # print("GOT INPUT FRAME OF SIZE " , frame.shape)
                if prediction_frame_done == 0:
                    rch.set_json({key1 : frame})
                    # cv2.imshow('input_frame',frame)
                # print('length of models',len(requested_models) )
                # print(requested_models)


                # part_presence  = random.choice([True,False])
                # print("part_presence:",part_presence)
                #if part_presence is False:
                #shyamdd
                time_tmp = tin - time.time()
                if rch.get_json(RedisKeyBuilderServer(wid).get_key(0,process_start_keyholder)):
                    # _, frame = cap_tmp.read()

                    try:
                        model_1.inference(frame)
                        frame_failed = False
                    except:
                        frame_failed = True
                    print("hereee!")

                    if bool(model_1.predictions) and not frame_failed:
                        if model_1.predictions['count'] == 1 and model_1.predictions["feature_name"] == "Part_Presence" :
                            part_presence = True
                            predicted_taco.append(model_1.predictions)
                            # print('Here!!!!!!!!! pillar')
                            # part_counter += 1
                        else:
                            part_presence = False
                            ii = 0
                        # print(part_presence)
                        if part_presence is True: # and ii == 0: 
                            i = 0
                            frame1 = frame.copy()
                            #frame1 = rch.get_json(RedisKeyBuilderServer(wid).get_key(camera_index,original_frame_keyholder))
                            for model in requested_models[short_number]:
                                #frame = rch.get_json(RedisKeyBuilderServer(wid).get_key(camera_index,original_frame_keyholder))
                                
                                try:
                                    st = time.time()
                                    model.inference(frame)
                                    # print(time.time() -st, "********************---------")
                                    key = RedisKeyBuilderServer(wid).get_key(camera_index,predicted_frame_keyholder)
                                    #setting the frame to reddis
                                    rch.set_json({key : model.predicted_frame})
                                    prediction_frame_done = 1
                                    # print(key)
                                    # print("Predicted Frame",model.predicted_frame.shape)
                                    predicted_taco.append(model.predictions)
                                    if bool(model.predictions_two):
                                        predicted_taco.append(model.predictions_two)
                                    # print("predicted_taco::::::::::::", predicted_taco)
                                    # resized_frame = cv2.resize(model.predicted_frame,(640,480))
                                    # cv2.imshow("Predicted_frame_"+str(i), model.predicted_frame)
                                    # cv2.imshow("Predicted_frame_"+str(i), resized_frame)
                                    i += 1
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

                                    cv2.imshow("Frame last::", frame1)    
                                
                                
                                except Exception as e:
                                    print(e)
                                    pass    
                                
                            rch.set_json({key : frame1})  
                            part_counter = set_mongo_payload(predicted_taco ,short_number, part_counter, camera_index) 

                            #New gokul   
                            predicted_taco.clear()
                            frame = None
                            rch.set_json({RedisKeyBuilderServer(wid).get_key(camera_index,original_frame_keyholder):None})

                            # ii+=1
                            #part_presence = False
<<<<<<< HEAD
                            cv2.imshow("predicted_frame",cv2.resize(model_1.predicted_frame,(640,480)))
                            cv2.imshow("pred frame", cv2.resize(frame1,(640,480)))
                            rch.set_json({RedisKeyBuilderServer(wid).get_key(0,process_start_keyholder) : False}) 
=======
                            # cv2.imshow("predicted_frame",model_1.predicted_frame)
                            rch.set_json({RedisKeyBuilderServer(wid).get_key(0,process_start_keyholder) : False})
                # del frame
                # del frame1
                # del key
                # del key1
                # if gc_counter % 1000 == 0:
                    # gc.collect()

                
>>>>>>> ca16d23b7c699c5bb5ddff9886e7981462d4aa65

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



def worker_main():
    while True:
        try:
            worker()
        except Exception as e:
            print(e)
            pass
if __name__=="__main__":
    # worker()  
    worker_main()  