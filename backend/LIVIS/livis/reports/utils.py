from common.utils import *
from django.utils import timezone
from bson import ObjectId
from toyoda.utils import generate_QRcode_util
from toyoda.utils import get_inspection_qc_list
from copy import deepcopy
from livis.settings import *
import sqlite3
from xlsxwriter import Workbook
from django.utils import timezone


def get_last_defect_list_util(inspection_id,skip=0, limit=20):
    inspection_collection = MongoHelper().getCollection(inspection_id)
    objs = inspection_collection.find().sort([( '$natural', -1 )])
    if objs.count() > 0:
        obj = objs[0]
        print("-----obj: ", obj)
        base64_image = generate_QRcode_util(inspection_id)
        obj.update({'qr_string' : base64_image})
        return obj
    else:
        return {}


def get_metrics_util(inspection_id):
    mp = MongoHelper().getCollection('inspection_data')
    pr = mp.find_one({"_id" : ObjectId(inspection_id)})
    print(pr)
    if pr:
        wid = pr['workstation_id']
        camera_id = 9
        workstation = MongoHelper().getCollection('workstations').find_one({'_id' : ObjectId(wid)})
        camera_config = [i['camera_id'] for i in workstation['cameras'] if i['camera_name'] != 'kanban']
        if len(camera_config) > 0:
            camera_id = camera_config[0]
        rescan_status_key = RedisKeyBuilderServer(wid).get_key(camera_id, 'rescan-required')
        if rescan_status_key:
            cc = CacheHelper()
            rescan_status = cc.get_json(rescan_status_key)
            print("REsCAN STATUS KEY : : :: : : : : : ", rescan_status_key, " ; ; ; ; " , rescan_status)
            inspection = MongoHelper().getCollection(inspection_id)
            total = inspection.count()
            total_accepted = inspection.find({'isAccepted' : True}).count()
            total_rejected = total - total_accepted
            qc_inspection = get_inspection_qc_list(inspection_id)
            resp = {
                "accepted" : total_accepted,
                "rejected" : total_rejected,
                "total" : total,
                "rescan_status" : rescan_status,
                "qc_inspection" : qc_inspection
            }
            return resp
        else:
            return {}
    else:
        return {}


def get_accepted_rejected_parts_list_util(start_date=None, end_date=None, status=None):
    mp = MongoHelper().getCollection('inspection_data')
    pr = [i['_id'] for i in mp.find()]
    all_accepted_parts = []
    all_rejected_parts = []
    all_parts = []    
    for id in pr:
        cp = MongoHelper().getCollection(str(id))
        accepted_parts = [i for i in cp.find({"isAccepted" : True})]
        rejected_parts = [i for i in cp.find( {"$or" : [
            {"isAccepted": False},
            { "isAccepted" : {"$exists" : False}}
            ]})]
        all_parts.extend([i for i in cp.find()])
        all_accepted_parts.extend(accepted_parts)
        all_rejected_parts.extend(rejected_parts)
    if status:
        if status:
            resp = {"data"  : all_accepted_parts}
        else:
            resp = {"data" : all_rejected_parts}
    else:
        resp = {"data" : all_parts}
    return resp

def get_name_byid(id):

    #print(id)

    command = "SELECT * FROM accounts_user WHERE user_id=" + '\"' + id + '\"'
    #print(command)

    conn = sqlite3.connect('/home/lincode/Desktop/livis_v2/republic/backend/LIVIS/livis/db.sqlite3')
    cursor = conn.cursor()
#     cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    cursor.execute(command)
    lis = cursor.fetchone()
    
    #print(lis)
    #admin_name = "N.A"  
    
    
    if lis is not None and len(lis)>0:
    
        return str(lis[4])
    else:
        return "N.A"

def get_mega_report_util(data):

    from_date = data.get('from_date')
    to_date = data.get('to_date')
    operator_id = data.get('operator_id',None)
    status = data.get('status',None) #pass / fail
    shift_id = data.get('shift_id',None)
    skip = data.get('skip',None)
    limit = data.get('limit',None)
    workstation_id = data.get('workstation_id',None)

    query = []

    if workstation_id:
        query.append({'workstation_id': workstation_id})
    if operator_id:
        query.append({'operator_id': operator_id })
    if shift_id:
        query.append({'shift_id': shift_id })
    if from_date:
        query.append({'start_time': {"$gte":from_date}})#,"$lte":to_date
    if to_date:
        query.append({'end_time': {"$lte":to_date}})

    print(query)

    if bool(query):
        inspectionid_collection = MongoHelper().getCollection(INSPECTION_COLLECTION)
        objs = [i for i in inspectionid_collection.find({"$and":query}).sort([( '$natural', -1)]) ]
    else:
        inspectionid_collection = MongoHelper().getCollection(INSPECTION_COLLECTION)
        objs = [i for i in inspectionid_collection.find()]


    p = []
    for ins in objs:
        inspection_id = str(ins['_id'])
        log_coll = MongoHelper().getCollection(inspection_id+"_log")
        if status:
            pr = [i for i in log_coll.find({'isAccepted':status})]
        else:
            pr = [i for i in log_coll.find()]
        p.extend(pr) 
    q = []
    if skip is not None and limit is not None:
        for items in p[skip:limit]:
            q.append(items)
    else:
        q = p.copy()

    print("length is :::: ",len(q))
    return q
    
    """
    for id1 in pr:
        process_attributes = mp.find_one({'_id' : ObjectId(id1)})
        process_attributes['process_id'] = process_attributes.pop('_id')
        #print("process_id:::::::::::",id1, ":::::::::::::process_attributes:::::::::::",process_attributes)
        
        #print("object::::::",[obj for obj in objs])
        for inspection_attributes in objs:
            inspection_attributes['inspected_part_id'] = inspection_attributes.pop('_id')
            print("inspection_attributes:::::::::::",inspection_attributes)
            defect_list_temp = dict(list(process_attributes.items()) + list(inspection_attributes.items()))
            all_defects_list.append(deepcopy(defect_list_temp))
    print("all_defects_list count:::::",len(all_defects_list))
    return all_defects_list
    """

def set_flag_util(data):
    master_obj_id = data['master_obj_id']
    slave_obj_id = data['slave_obj_id']
    remark = data['remark']

    mp = MongoHelper().getCollection(master_obj_id+"_log")

    process_attributes = mp.find_one({'_id' : ObjectId(slave_obj_id)})

    process_attributes['remarks']= remark
    process_attributes['flagged']= True
    print(process_attributes)
    mp.update({'_id' : ObjectId(slave_obj_id) }, {'$set' :  process_attributes})
    process_attributes = mp.find_one({'_id' : ObjectId(slave_obj_id)})
    
    #goto annotation and set as untagged
    part_id = process_attributes['part_id']
    captured_original_frame_http = process_attributes['captured_original_frame_http']
    captured_original_frame = process_attributes['captured_original_frame']
    
    mp = MongoHelper().getCollection(str(part_id)+"_dataset")
    
    capture_doc = {
                        "file_path": captured_original_frame,
                        "file_url": captured_original_frame_http,
                        "state": "untagged",
                        "annotation_detection": [],
                        "annotation_detection_history": [],
                        "annotation_classification": "",
                        "annotation_classification_history": [],
                        "annotator": "",
                        "date_added":timezone.now()}
                        
    
    mp.insert(capture_doc)
    

    return process_attributes  

def edit_remark_util(data):
    master_obj_id = data['master_obj_id']
    slave_obj_id = data['slave_obj_id']
    remark = data['remark']

    mp = MongoHelper().getCollection(master_obj_id+"_log")

    process_attributes = mp.find_one({'_id' : ObjectId(slave_obj_id)})

    process_attributes['remarks']= remark
    print(process_attributes)
    mp.update({'_id' : ObjectId(slave_obj_id) }, {'$set' :  process_attributes})
    process_attributes = mp.find_one({'_id' : ObjectId(slave_obj_id)})

    
    return process_attributes


def get_summary_end_process_util(inspection_id):
    resp = {}
    mp = MongoHelper().getCollection('inspection_data')
    process_attributes = mp.find_one({'_id' : ObjectId(inspection_id)})
    if process_attributes:
        user_image_url = ""
        collection_obj = {
           'part_number' : process_attributes['part_number'],
           'model_number' : process_attributes['model_number'],
           'short_number' : process_attributes['short_number'],
           'operator_name' : process_attributes['user']['name'],
           'createdAt' : process_attributes['createdAt'],
           'completedAt' : process_attributes['completedAt'],
           'duration' : process_attributes['duration'],
           'operator_role' : process_attributes['user']['role'],
           'total_parts' : process_attributes['total_parts'],
           'total_accepted_parts' : process_attributes['total_accepted_parts'],
           'total_rejected_parts' : process_attributes['total_rejected_parts'],
           'user_image_url' : user_image_url
        }
        resp = collection_obj
        return resp
    else:
        return "Data not found."


def defect_type_based_report_util(data):
    from_date = data.get('from_date')
    to_date = data.get('to_date')
    workstation_id = data.get('workstation_id',None)
    mp = MongoHelper().getCollection('inspection_data')
    query = []
    query.append({'timestamp': {"$gte":from_date,"$lte":to_date}})
    all_defect_list = []
    total_count = 0
    if workstation_id:
        pr = [i for i in mp.find({'workstation_id': workstation_id})]
    else :
        pr = [i for i in mp.find()]
    master_defects_list = get_master_defects()
    #print("----pr: ",pr)
    for defect in master_defects_list:
        #print("--------------------------Loop---------------------")
        #print("----defect: ",defect)
        for obj in pr:
            #print("----obj: ",obj)
            id1 = obj['_id']
            
            inspectionid_collection = MongoHelper().getCollection(str(id1)) 
            defect_counter =  inspectionid_collection.count(
            {
                "$and": [{'timestamp': {"$gte":from_date,"$lte":to_date}},{'defect_list': {"$in" : [defect]}}]
            })
            #print("----defect_counter: ",defect_counter)
            total_count+=defect_counter
        collection_obj = {
            'defect_type' : defect,
            'count' : total_count
            }    
        #print("----collection_obj: ",collection_obj)
        all_defect_list.append(collection_obj)
        defect_counter = 0
        total_count = 0    
    return all_defect_list


def get_master_defects():
    #mp = MongoHelper().getCollection(PARTS_COLLECTION)
    #pr = [i for i in mp.find()]
    #master_defect_list = []
    #for p in pr:
    #    if 'kanban' in p:
    #        if 'defect_list' in p['kanban']:
    #            master_defect_list.extend(p['kanban']['defect_list'])
    #return list(set(master_defect_list))
    master_defect_list = ['Shot_Shot_Presence']
    return master_defect_list


def get_master_features():
    #mp = MongoHelper().getCollection(PARTS_COLLECTION)
    #pr = [i for i in mp.find()]
    #master_feature_list = []
    #for p in pr:
    #    if 'kanban' in p:
    #        if 'feature_list' in p['kanban']:
    #            master_feature_list.extend(p['kanban']['feature_list'])
    #return list(set(master_feature_list))
    master_feature_list = ['PPWOSRSRH','PPWOSRSLH','Felt_Presence','Clip_Presence']
    return master_feature_list
    
def get_defect_report_util():
    payload = {}
    return payload
    
def post_report_util():
    date_from = ""
    date_to = ""
    operator_id = ""
    shift_id = ""
    w_id = ""
    status = ""
    current = 0
    limit = 0
    ###  logic to update mongo
    return resp
    
def post_remark_util():
    _id = ""
    remark = ""
    status = 200
    message = "Success"
    return message, status



