from common.utils import MongoHelper
from livis.settings import *
from bson import ObjectId
import datetime
import base64
import uuid 
import datetime
from inspection.virtualbutton import *
from kafka import KafkaProducer,  KafkaConsumer
import numpy as np
import sqlite3
def plan_production_counter_modify_util(data):

    mp = MongoHelper().getCollection(PLAN_COLLECTION)
    inspection_id = data['inspection_id']
    plan_id = data['plan_id']
    
    current_production_count = data['current_production_count']
    
    pr = mp.find_one({"_id" : ObjectId(plan_id)})
    
    if pr:
        pr['planned_production_count'] = current_production_count
        mp.update({'_id' : pr['_id']}, {'$set' : pr})
        return mp.find_one({"_id" : ObjectId(plan_id)})
    else:
        return {}


def report_process_util(data,operator_id):

    inspection_id = data.get('inspection_id',None)
    inspection_log_id = data.get('inspection_log_id',None)
    workstation_id = data.get('workstation_id',None)
    camera_id = data.get('camera_id',None)
    
    
    mp = MongoHelper().getCollection( str(inspection_id) + "_" + "log")
    
    #get features and defects from kafka realtime
    topic = str(workstation_id) + "_" + str(camera_id) + "_input"
    consumer = KafkaConsumer(topic, bootstrap_servers=KAFKA_BROKER_URL, auto_offset_reset='latest')
    #consumer.poll()
    #consumer.seek_to_end()
        
    for message in consumer:
        #print(consumer.committed())
        a = message.value.decode('utf-8')
        b = json.loads(a)
        
        im_b64_str = b["frame"]
        im_b64 = bytes(im_b64_str[2:], 'utf-8')
        im_binary = base64.b64decode(im_b64)

        im_arr = np.frombuffer(im_binary, dtype=np.uint8)
        img_original = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
        
        #write the original image on disk and get http path
        uuid_str = str(uuid.uuid4()) 
        img_name_original = TRAIN_DATA_STATIC+"/"+str(uuid_str)+".png"
        img_name_original_http = "http://"+BASE_URL+":3306/"+str(uuid_str)+".png"
        cv2.imwrite(img_name_original,img_original)
        
        
        break
            
    #get features and defects from kafka realtime
    topic = str(workstation_id) + "_" + str(camera_id) + "_output"
    consumer = KafkaConsumer(topic, bootstrap_servers=KAFKA_BROKER_URL, auto_offset_reset='latest')
    #consumer.poll()
    #consumer.seek_to_end()
        
    for message in consumer:
        #print(consumer.committed())
        a = message.value.decode('utf-8')
        b = json.loads(a)
        
        detections = b["detections"]
        im_b64_str = b["frame"]
        im_b64 = bytes(im_b64_str[2:], 'utf-8')
        im_binary = base64.b64decode(im_b64)

        im_arr = np.frombuffer(im_binary, dtype=np.uint8)
        img_inference = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
        
        #write the inference image on disk and get http path
        uuid_str = str(uuid.uuid4()) 
        img_name_pred = TRAIN_DATA_STATIC+"/"+str(uuid_str)+".png"
        img_name_pred_http = "http://"+BASE_URL+":3306/"+str(uuid_str)+".png"
        cv2.imwrite(img_name_pred,img_inference)
        
        break
    
    
    
    colle = {
    "captured_original_frame_http":img_name_original_http,
    "captured_inference_frame_http":img_name_pred_http,
    "captured_original_frame" : img_name_original,
    "captured_inference_frame" : img_name_pred
    }
    
    dataset = mp.find_one({'_id' : ObjectId(inspection_log_id)})
    
    mp.update({'_id' : ObjectId(dataset['_id'])}, {'$set' :  colle})
    
    return dataset
    
    
    
#get matrix -- _log sort natureal send latest back 
#_inspection master status compleated or not - get running inspection 
#get runnnig process - check status master inspection table -- started and compleated
#end inspection 


    

def get_running_process_util(workstation_id):

    #print("got into ")

    mp = MongoHelper().getCollection(INSPECTION_COLLECTION)
    
    insp_coll = [i for i in mp.find({"$and":[ {"status":"started"} , {"workstation_id":workstation_id} ] } )]
    
    if insp_coll == []:
        return [],200
    else:
        return insp_coll,200
    
def get_metrics_util(inspection_id):

    mp = MongoHelper().getCollection( str(inspection_id) + "_" + "log")

    dataset = [p for p in mp.find().sort( "$natural", -1 )]
    dataset1 = [p for p in mp.find({"isAccepted":True})]
    dataset2 = [p for p in mp.find({"isAccepted":False})]
    total_production = len(dataset)
    total_accepted_count = len(dataset1)
    total_rejected_count = len(dataset2)
    if len(dataset) > 0:

        dataset = dataset[0]

        s = datetime.datetime.strptime(dataset['inference_start_time'], '%Y-%m-%d %H:%M:%S')
        e = datetime.datetime.strptime(dataset['inference_end_time'], '%Y-%m-%d %H:%M:%S')

        #s = dataset['inference_start_time']
        #e = dataset['inference_end_time']

        dataset['duration'] = str(e-s)
        dataset['total'] = str(total_production)
        dataset['total_accepted'] = str(total_accepted_count)
        dataset['total_rejected'] = str(total_rejected_count)
    else:
        dataset = {}
    return dataset,200
    
    

    


def start_process_util(data,operator_id):
    part_id = data.get('part_id',None)
    workstation_id = data.get('workstation_id',None)
    #camera_id = data.get('camera_id',None)
    #check if its deployed
    mp = MongoHelper().getCollection(EXPERIMENT_COLLECTION)
    true_list = [i for i in mp.find({"$and" :[{"part_id":part_id , 'container_deployed' : True, 'container_deployed' : {'$exists' : True}}] })]  
    for i in true_list:
        print(i['container_deployed'])
    #print(true_list[0].keys())
    true_list = [ i for i in true_list if i['container_deployed']] 
    print(true_list, len(true_list)) 
    if len(true_list) == 1:
        pass
    elif len(true_list) == 0:
        #not deployed
        return "experiment is not deployed, please deploy it first",400
    else:
        return "multiple experiment deployed, please check the deployment list",400
    
    ## GET PLAN INFO 
    #fetch plan_id
    mp = MongoHelper().getCollection(PLAN_COLLECTION)
    print("part_id")
    print(part_id)
    plan_coll_fin = [i for i in mp.find({ "$and" : [ {"part_id":part_id} , {"is_deleted": False}, { "is_deleted" : {"$exists" : True}}] })]
    print("plan is ")
    print(plan_coll_fin)
    #print(datetime.datetime.now())
    #plan_coll = [i for i in plan_coll if plan[i]['start_time'] < datetime.datetime.now() and plan[i]['end_time'] > datetime.datetime.now()]
    import datetime
    plan_coll = []
    for i in plan_coll_fin:
        print(i['start_time'])
        st = datetime.datetime.strptime(i['start_time'], '%Y-%m-%d')
        et = datetime.datetime.strptime(i['end_time'], '%Y-%m-%d')

        print(st)

        if st < datetime.datetime.now() and et > datetime.datetime.now():
            plan_coll.append(i)

    plan_id = None
    
    if len(plan_coll) > 0:  
        plan_id = str(plan_coll[0]["_id"])
        planned_production_count = plan_coll[0]["planned_production_count"]    
    
    
    #GET SHIFT INFO
    #fetch shift_id
    mp = MongoHelper().getCollection(SHIFT_COLLECTION)
    import time


    import datetime
    time_now = str(datetime.datetime.now().time()).split('.')[0]

    print(time_now)
    shift_coll = [i for i in mp.find({ "$and" : [ {"status": True}, { "status" : {"$exists" : True}},{"start_time": {"$lte": time_now}}, {"end_time": {"$gte": time_now}} ] })]
    if len(shift_coll) == 0:
        #no shift at this time of the day
        return "no shift at this time of the day, please come back during inspection time",400
    shift_id = str(shift_coll[0]["_id"])


    from capture.utils import get_inference_feed_url_util



    #create inspection entry
    mp = MongoHelper().getCollection(INSPECTION_COLLECTION)
    current_date = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    createdAt = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    coll = {
    "part_id":part_id,
    "workstation_id":workstation_id,
    "plan_id":plan_id,
    "start_time":createdAt,
    "end_time":"",
    "shift_id":shift_id,
    "operator_id":operator_id,
    "produced_on":current_date,
    "status":"started",
    "inference_urls" :  get_inference_feed_url_util(workstation_id , part_id)
    }
    _id = mp.insert(coll)
    VB = VirtualButton()
    VB.inspection_id = str(_id)
    VB.workstation_id = workstation_id
    VB.start_button_service()
    ret = mp.find_one({'_id' : _id})
    return ret ,200
    

def save_inference_image(img_np, inspection_id, inference_done):
    
    print("inference done")
    print(inference_done)
    inference_path = 'original'
    if inference_done:
        inference_path = 'infered'
    SAVE_PATH = os.path.join(TRAIN_DATA_STATIC,'inpection_data',inspection_id, inference_path)
    if not os.path.exists(SAVE_PATH):
        os.makedirs(SAVE_PATH)
    uuid_str = str(uuid.uuid4()) 
    img_name_original = os.path.join(SAVE_PATH, str(uuid_str)+".png")
    cv2.imwrite(img_name_original,img_np)
    
    return img_name_original
                
def get_name_byid(id):

    command = "SELECT * FROM accounts_user WHERE user_id=" + '\"' + id + '\"'

    conn = sqlite3.connect('/home/lincode/Desktop/livis_v2/republic/backend/LIVIS/livis/db.sqlite3')
    cursor = conn.cursor()
    cursor.execute(command)
    lis = cursor.fetchone()
    
    if lis is not None and len(lis)>0:
    
        return str(lis[4])
    else:
        return "N.A"

def get_virtual_button_util(data):

    inspection_start_time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    print('made an api call on tap')
    try:
        inspection_id = data['inspection_id']
    except:
        inspection_id = None
    #get features and defects from kafka realtime
    try:
        workstation_id = data['workstation_id']
    except:
        workstation_id = None

    if not inspection_id or not workstation_id:
        return 'No inspection / workstation assigned found for this click' , 400

    mp = MongoHelper().getCollection(WORKSTATION_COLLECTION)
    f = mp.find_one({'_id' : ObjectId(workstation_id)})
    cameras = f['cameras'] if 'cameras' in f else []
    print('cameras are')
    print(cameras)

    detections = {}
    saved_images_original = []
    saved_images_inference = []

    if len(cameras) > 0:
        for camera in cameras:

            topic = str(workstation_id) + "_" + str(camera['camera_id']) + "_input"
            consumer = KafkaConsumer(topic, bootstrap_servers=KAFKA_BROKER_URL, auto_offset_reset='latest',session_timeout_ms=3000)
            #consumer.poll()
            #consumer.seek_to_end()
            for message in consumer:
                print("in orig")
                #print(consumer.committed())
                a = message.value.decode('utf-8')
                b = json.loads(a)
                im_b64_str = b["frame"]
                im_b64 = bytes(im_b64_str[2:], 'utf-8')
                im_binary = base64.b64decode(im_b64)
                im_arr = np.frombuffer(im_binary, dtype=np.uint8)
                img_original = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
                saved_images_original.append(save_inference_image(img_original, inspection_id, False))
                #write the original image on disk and get http path
                break
            consumer.close()
            
            #get features and defects from kafka realtime
            topic = str(workstation_id) + "_" + str(camera['camera_id']) + "_output"
            print(topic)
            consumer1 = KafkaConsumer(topic, bootstrap_servers=KAFKA_BROKER_URL, auto_offset_reset='latest',session_timeout_ms=3000)
            #consumer.poll()
            #consumer.seek_to_end()
        
            for message in consumer1:
                print("in inf")
                #print(consumer.committed())
                a = message.value.decode('utf-8')
                b = json.loads(a)
                for key in b['detections']:
                    if key in detections:
                        detections[key].extend(b['detections'][key])
                    else:
                        detections[key] = b['detections'][key]
                im_b64_str = b["frame"]
                im_b64 = bytes(im_b64_str[2:], 'utf-8')
                im_binary = base64.b64decode(im_b64)
                im_arr = np.frombuffer(im_binary, dtype=np.uint8)
                img_inference = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
                #write the inference image on disk and get http path
                saved_images_inference.append(save_inference_image(img_inference, inspection_id, True))
                break
            consumer1.close()
            
    print("before kanban logics")
    ##Iterate over detections , match kanban and insert object in log table.

    """
    detections=  {
        "features": {"hole": [{
                "x": 0.0862708719851577,
                "y": 0.24382537105751392,
                "w": 0.03339517625231911,
                "h": 0.04267161410018552,
                "cls": "hole",
                "centroid": [0.10296846011131726, 0.2651611781076067],
                "type": "box",
                "highlighted": False,
                "editingLabels": False,
                "color": "#f44336",
                "id": "4742407370643873"
            }, {
                "x": 0.2810760667903525,
                "y": 0.21414076994434136,
                "w": 0.04870129870129869,
                "h": 0.06122448979591835,
                "cls": "hole",
                "centroid": [0.30542671614100186, 0.24475301484230055],
                "type": "box",
                "highlighted": False,
                "editingLabels": False,
                "color": "#f44336",
                "id": "9646853828901427"
            }, {
                "x": 0.09879406307977737,
                "y": 0.4386305658627087,
                "w": 0.038961038961038974,
                "h": 0.04267161410018555,
                "cls": "hole",
                "centroid": [0.11827458256029685, 0.4599663729128015],
                "type": "box",
                "highlighted": False,
                "editingLabels": False,
                "color": "#f44336",
                "id": "5152909813770326"
            }],
            "bad_injection": [{
                "x": 0.3423005565862709,
                "y": 0.28278641001855287,
                "w": 0.04591836734693877,
                "h": 0.05009276437847865,
                "cls": "bad_injection",
                "centroid": [0.3652597402597403, 0.3078327922077922],
                "type": "box",
                "highlighted": False,
                "editingLabels": False,
                "color": "#2196f3",
                "id": "2754882814367636"
            }, {
                "x": 0.33116883116883117,
                "y": 0.4033801020408163,
                "w": 0.0640074211502783,
                "h": 0.0575139146567718,
                "cls": "bad_injection",
                "centroid": [0.3631725417439703, 0.4321370593692022],
                "type": "box",
                "highlighted": True,
                "editingLabels": False,
                "color": "#2196f3",
                "id": "9716443111278084"
            }]},
        "defects": ["bad_injection"],
            
        
    }
    """

    match_kanban, detection_cleaned = kanban_check(inspection_id, detections)
    is_pass = True
    if match_kanban is True:
        is_pass = False
    print("after kanban check")
    #create another inspection_id_log collection
    f = []
    mp = MongoHelper().getCollection(WORKSTATION_COLLECTION)
    f = mp.find_one({'_id' : ObjectId(workstation_id)})
    workstation_name = ""
    if len(f)>0:
        workstation_name = f['workstation_name']
        
    f = []
    mp = MongoHelper().getCollection(INSPECTION_COLLECTION)
    f = mp.find_one({'_id' : ObjectId(inspection_id)})
    shift_id = ""
    operator_id = ""
    if len(f)>0:
        shift_id = f['shift_id']
        operator_id = f['operator_id']
        part_id = f['part_id']
    
    shift_name = ""
    if shift_id != "":
        f = []
        mp = MongoHelper().getCollection(SHIFT_COLLECTION)
        f = mp.find_one({'_id' : ObjectId(shift_id)})
        if len(f)>0:
            shift_name = f['shift_name']

    part_name = ""
    if part_id != "":
        f = []
        mp = MongoHelper().getCollection(PARTS_COLLECTION)
        f = mp.find_one({'_id' : ObjectId(part_id)})
        if len(f)>0:
            part_name = f['part_number']

    operator_name = ""
    if operator_id != "":
        operator_name = get_name_byid(operator_id)
    
    mp = MongoHelper().getCollection( str(inspection_id) + "_" + "log")
    
    saved_images_original_http = []
    saved_images_inference_http = []
    for orig in saved_images_original:
        http_pth = "http://"+BASE_URL+":3306/"+orig.split(TRAIN_DATA_STATIC)[1]
        saved_images_original_http.append(http_pth)
    for inf in saved_images_inference:
        http_pth = "http://"+BASE_URL+":3306/"+inf.split(TRAIN_DATA_STATIC)[1]
        saved_images_inference_http.append(http_pth)
    colle = {
    "detections_missed" : detection_cleaned,
    "shift_id":shift_id,
    "shift_name":shift_name,
    "operator_id":operator_id,
    "operator_name":operator_name,
    "workstation_id":workstation_id,
    "workstation_name":workstation_name,
    "part_id":part_id,
    "part_name":part_name,
    "isAccepted":is_pass,
    "remarks":"",
    "flag_retrain":False,
    "captured_original_frame": saved_images_original,
    "captured_original_frame_http":saved_images_original_http,
    "captured_inference_frame": saved_images_inference,
    "captured_inference_frame_http":saved_images_inference_http,
    "inference_start_time":inspection_start_time,
    "inference_end_time":datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
    "master_objid":str(inspection_id),
    "flagged":False
    }
    _id = mp.insert(colle)
    message = _id
    status_code = 200
    
    return message,status_code


def match_kanban_qty(kanban_feat_list, inference_feat_list):
    return abs(len(kanban_feat_list) - len(inference_feat_list))
    

def match_kanban_pos(kanban_feat_list, inference_feat_list, thres=20):
    
    kanban_feat_list.sort(key = lambda x :(float(x['y']),float(x['x'])))
    inference_feat_list.sort(key = lambda x :(float(x['x']),float(x['y'])))

    print("Kanban:",kanban_feat_list)
    print("Inference:",inference_feat_list)


    pos_mismatch = []

    for idx, i in enumerate(inference_feat_list):
        if 'centroid' in i:
            x, y = i['centroid']
            x=float(x)*640
            y=float(y)*480
            
            print("Predicted Centroid:",(x,y))
            
            x1, y1 = kanban_feat_list[idx]['centroid']
            x1=x1*640
            y1=y1*480
            
            print("Kanban Centroid:",(x1,y1))
            if abs(float(x) - x1)  > thres   or abs(float(y) - y1) > thres :
                #print("WIdth Diff:",abs(float(x) - x1) * 640)
                #print("Ht Diff:",abs(float(y) - y1) * 480)
                pos_mismatch.append(idx)
            print("WIdth Diff:",abs(float(x) - x1) * 640)
            print("Ht Diff:",abs(float(y) - y1) * 480)
            # print()
    print("pos_mis",pos_mismatch)
    return pos_mismatch


def kanban_check(inspection_id, detections):
    mp = MongoHelper().getCollection(INSPECTION_COLLECTION)

    pr = mp.find_one({'_id' : ObjectId(inspection_id)})
    part_id = pr['part_id']
    pp = MongoHelper().getCollection(PARTS_COLLECTION)
    part = pp.find_one({'_id' : ObjectId(part_id)})
    kanban = part['kanban'] if 'kanban' in part else {}
    part_failed_flag = False
    reason_part_failed = []
    detections_cleaned = {'features' : [] , 'defects' : []}
    if kanban:
        print("kanban features are")
        print(kanban['features'])
        print("inference detections are")
        print(detections)
        for feature in kanban['features']:
            if feature in detections:
                coords = detections[feature]  ## should give a list of {x,y,w,h,cent}
                print("Length of Coords:",len(coords))
                feat_qty_flag = match_kanban_qty(kanban['kanban_details'][feature], coords)
                if feat_qty_flag > 0:
                    part_failed_flag = True
                    reason_part_failed.append('{} {} missing in part!'.format(feat_qty_flag ,feature))
                else:
                    pass
                    
                    #pos_mismatch_idx = match_kanban_pos(kanban['kanban_details'][feature], coords)
                    #feat_pos_flag = False if len(pos_mismatch_idx) > 0 else True
                    #if not feat_pos_flag:
                    #    part_failed_flag = True
                    #    reason_part_failed.append('{} {} out of position in part!'.format(pos_mismatch_idx ,feature))
            else:
                part_failed_flag = True
                reason_part_failed.append('{} missing in part!'.format(feature))
        for defect in kanban['defects']:
            if defect in detections:
                part_failed_flag = True
                reason_part_failed.append('{} defect present in part!'.format(defect))
    return part_failed_flag , reason_part_failed


   
def end_process_util(data,operator_id):
    inspection_id = data.get('inspection_id',None)
    endedAt = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    colle = {
    "status" : "completed",
    "end_time" : endedAt
    }
    mp = MongoHelper().getCollection(INSPECTION_COLLECTION)
    dataset = mp.find_one({'_id' : ObjectId(inspection_id)})
    mp.update({'_id' : ObjectId(dataset['_id'])}, {'$set' :  colle})
    dataset = mp.find_one({'_id' : ObjectId(inspection_id)})

    s = datetime.datetime.strptime(dataset['start_time'], '%Y-%m-%d %H:%M:%S')
    e = datetime.datetime.strptime(dataset['end_time'], '%Y-%m-%d %H:%M:%S')

    dataset['duration'] = str(e-s)


    mp = MongoHelper().getCollection( str(inspection_id) + "_" + "log")

    dataset0 = [p for p in mp.find().sort( "$natural", -1 )]
    dataset1 = [p for p in mp.find({"isAccepted":True})]
    dataset2 = [p for p in mp.find({"isAccepted":False})]
    total_production = len(dataset0)
    total_accepted_count = len(dataset1)
    total_rejected_count = len(dataset2)


    dataset['total'] = str(total_production)
    dataset['total_accepted'] = str(total_accepted_count)
    dataset['total_rejected'] = str(total_rejected_count)
    try:
        VB = VirtualButton().stop_button_service()
    except:
        pass
    
    return dataset,200
