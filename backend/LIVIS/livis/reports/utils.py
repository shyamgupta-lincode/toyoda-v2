from common.utils import *
from django.utils import timezone
from bson import ObjectId
from toyoda.utils import generate_QRcode_util
from toyoda.utils import get_inspection_qc_list
from copy import deepcopy


def get_last_defect_list_util(inspection_id,skip=0, limit=20):
    inspection_collection = MongoHelper().getCollection(inspection_id)
    objs = inspection_collection.find().sort([( '$natural', -1 )] )
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


def get_defect_list_report_util(data):
    from_date = data.get('from_date')
    to_date = data.get('to_date')
    operator_name = data.get('operator_name',None)
    #print('----operator_name',operator_name)
    defect_type = data.get('defect_type',None)
    #print('----defect_type',defect_type)
    feature_type = data.get('feature_type',None)
    mp = MongoHelper().getCollection('inspection_data')
    if operator_name is not None :
        pr = [i['_id'] for i in mp.find({'user.name': operator_name})]
    else :
        pr = [i['_id'] for i in mp.find()]
    process_attributes = {}
    inspection_attributes = {}
    all_defects_list = []
    query = []
    query.append({'timestamp': {"$gte":from_date,"$lte":to_date}})
    if defect_type:
        query.append({'defect_list': {"$in":defect_type}})
    if feature_type:
        query.append({'feature_list': {"$in": feature_type}})
    for id1 in pr:
        process_attributes = mp.find_one({'_id' : ObjectId(id1)})
        process_attributes['process_id'] = process_attributes.pop('_id')
        #print("process_id:::::::::::",id1, ":::::::::::::process_attributes:::::::::::",process_attributes)
        inspectionid_collection = MongoHelper().getCollection(str(id1)) 
        objs =  inspectionid_collection.find(
            {
                "$and": query

            }).sort([( '$natural', -1 )] )
        #print("object::::::",[obj for obj in objs])
        for inspection_attributes in objs:
            inspection_attributes['inspected_part_id'] = inspection_attributes.pop('_id')
            print("inspection_attributes:::::::::::",inspection_attributes)
            defect_list_temp = dict(list(process_attributes.items()) + list(inspection_attributes.items()))
            all_defects_list.append(deepcopy(defect_list_temp))
    print("all_defects_list count:::::",len(all_defects_list))
    return all_defects_list


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
