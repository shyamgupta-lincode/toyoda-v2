from common.utils import MongoHelper
from livis.settings import *
from bson import ObjectId


def add_workstation_task(data):
   workstation_name = data.get('workstation_name')
   workstation_ip = data.get('workstation_ip')
   workstation_port = data.get('workstation_port')
   workstation_status = data.get('workstation_status')
   workstation_location = data.get('workstation_location')
   cameras_info = data.get('cameras')
   isdeleted = False
   mp = MongoHelper().getCollection(WORKSTATION_COLLECTION)
   collection_obj = {
       'workstation_name' : workstation_name,
       'workstation_ip' : workstation_ip,
       'workstation_port' : workstation_port,
       'workstation_status' : workstation_status,
       'workstation_location':workstation_location,
       'cameras' : cameras_info,
       'isdeleted' : isdeleted
    }
   _id = mp.insert(collection_obj)
   return _id

def delete_workstation_task(wid):
    _id = wid
    mp = MongoHelper().getCollection(WORKSTATION_COLLECTION)
    ws = mp.find_one({'_id' : ObjectId(_id)})
    isdeleted = ws.get('isdeleted')
    if not isdeleted:
        ws['isdeleted'] = True
    mp.update({'_id' : ws['_id']}, {'$set' :  ws})
    return _id


def update_workstation_task(data):
    _id = data.get('_id')
    if _id:
        mp = MongoHelper().getCollection(WORKSTATION_COLLECTION)
        wc = mp.find_one({'_id' : ObjectId(_id)})
        workstation_name = data.get('edit_workstation_name')
        workstation_ip = data.get('edit_workstation_ip')
        workstation_port = data.get('edit_workstation_port')
        workstation_status = data.get('edit_workstation_status')
        workstation_location = data.get('edit_workstation_location')
        cameras = data.get('camerasEdit')
        if workstation_name:
            wc['workstation_name'] = workstation_name
        if workstation_ip:
            wc['workstation_ip'] = workstation_ip
        if workstation_port:
            wc['workstation_port'] = workstation_port
        if workstation_status:
            wc['workstation_status'] = workstation_status
        if workstation_location:
            wc['workstation_location'] = workstation_location    
        if cameras:
            i=0
            for camera in cameras:
                camera['camera_id'] = camera.pop('edit_camera_id')
                camera['camera_name'] = camera.pop('edit_camera_name')
                i+=1
            wc['cameras'] = cameras
        mp.update({'_id' : wc['_id']}, {'$set' :  wc})
    return _id


def get_workstation_config_task(workstation_id):
    _id = ObjectId(workstation_id)
    mp = MongoHelper().getCollection(WORKSTATION_COLLECTION)
    p = mp.find_one({'_id' : _id})
    if p:
        return p
    else:
        return {}


def get_workstations_task(skip=0, limit=100):
    mp = MongoHelper().getCollection(WORKSTATION_COLLECTION)
    workstations = [p for p in mp.find({"$and" : [{"isdeleted": False}, { "isdeleted" : {"$exists" : True}}]}).skip(skip).limit(limit)]
    if workstations:
        return workstations
    else:
        return []

        