# import cv2
import os
import argparse
import shutil
import redis
import requests
#from django.conf import settings
from bson import ObjectId
import json
from pymongo import MongoClient
import datetime
#from django.http import HttpResponse
# from kanban import static_kanban

def singleton(cls):
    try:
        instances = {}
        def getinstance():
            if cls not in instances:
                instances[cls] = cls()
            return instances[cls]
        return getinstance
        
    except:
        pass    




#Settings for MongoDB
# SERVER_HOST = "192.168.198.150"
SERVER_HOST = "localhost"
MONGO_SERVER_HOST = SERVER_HOST
MONGO_SERVER_PORT = 27017
#MONGO_DB = "LIVIS"
MONGO_DB = "TOYODA"
MONGO_COLLECTION_PARTS = "parts"
MONGO_COLLECTIONS = {MONGO_COLLECTION_PARTS: "parts"}
WORKSTATION_COLLECTION = 'workstations'
PARTS_COLLECTION = 'parts'
SHIFT_COLLECTION = 'shift'
PLAN_COLLECTION = 'plan'
WORKSTATION_ID_PATH = '/home/toyoda/livis_v2_toyota/republic/backend/camera_service_toyoda/workstation_id.json'


@singleton
class MongoHelper:
    try:
        client = None
        def __init__(self):
            if not self.client:
                self.client = MongoClient(host=SERVER_HOST, port=MONGO_SERVER_PORT)
            self.db = self.client[MONGO_DB]

        def getDatabase(self):
            return self.db

        def getCollection(self, cname, create=False, codec_options=None):
            _DB = MONGO_DB
            DB = self.client[_DB]
            if cname in MONGO_COLLECTIONS:
                if codec_options:
                    return DB.get_collection(MONGO_COLLECTIONS[cname], codec_options=codec_options)
                return DB[MONGO_COLLECTIONS[cname]]
            else:
                return DB[cname]

    except:
        pass            

# @singleton
# class MongoHelper:
#     client = None

#     def __init__(self):
#         if not self.client:
#             self.client = MongoClient(host='localhost', port=27017)

#         # self.db = self.client['LIVIS']
#         self.db = self.client['TOYODA']

#         if settings.DEBUG:
#             self.db.set_profiling_level(2)
#         # placeholder for filter
        
#     """
#     def getDatabase(self):
#         return self.db
#     """

#     def getCollection(self, cname, create=False, codec_options=None):
#         _DB = 'TOYODA' #'LIVIS'
#         DB = self.client[_DB]
#         return DB[cname]



def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance


import pickle

@singleton
class CacheHelper():
    try:
        def __init__(self):
            self.redis_cache = redis.StrictRedis(host=SERVER_HOST, port="6379", db=0, socket_timeout=1)
            #self.redis_cache = redis.StrictRedis(host=settings.REDIS_CLIENT_HOST, port=settings.REDIS_CLIENT_PORT, db=0, socket_timeout=1)
            #settings.REDIS_CLIENT_HOST
            print("REDIS CACHE UP!")

        def get_redis_pipeline(self):
            return self.redis_cache.pipeline()

        #should be {'key'  : 'value'} always
        def set_json(self, dict_obj):
            try:
                k, v = list(dict_obj.items())[0]
                v = pickle.dumps(v)
                return self.redis_cache.set(k, v)
            except redis.ConnectionError:
                return None

        def get_json(self, key):
            try:
                temp = self.redis_cache.get(key)
                #print(temp)\
                if temp:
                    temp= pickle.loads(temp)
                return temp
            except redis.ConnectionError:
                return None
            return None

        def execute_pipe_commands(self, commands):
            #TBD to increase efficiency can chain commands for getting cache in one go
            return None
    except:
        pass        


@singleton
class CacheHelperLocal():
    try:
        def __init__(self):
            self.redis_cache = redis.StrictRedis(host=SERVER_HOST, port="6379", db=0, socket_timeout=1)
            print("REDIS CACHE UP!")

        def get_redis_pipeline(self):
            return self.redis_cache.pipeline()

        #should be {'key'  : 'value'} always
        def set_json(self, dict_obj):
            try:
                k, v = list(dict_obj.items())[0]
                v = pickle.dumps(v)
                return self.redis_cache.set(k, v)
            except redis.ConnectionError:
                return None

        def get_json(self, key):
            try:
                temp = self.redis_cache.get(key)
                #print(temp)\
                if temp:
                    temp= pickle.loads(temp)
                return temp
            except redis.ConnectionError:
                return None
            return None

        def execute_pipe_commands(self, commands):
            #TBD to increase efficiency can chain commands for getting cache in one go
            return None

    except:
        pass        





class CacheHelperWorkstation():
    try:
        def __init__(self, CLIENT_ID, CLIENT_PORT):
            self.redis_cache = redis.StrictRedis(host=SERVER_HOST, port=CLIENT_PORT, db=0, socket_timeout=1)
            print("REDIS CACHE UP!")
            print("Connected to  :" + CLIENT_ID + ":" + CLIENT_PORT)

        def get_redis_pipeline(self):
            return self.redis_cache.pipeline()

        #should be {'key'  : 'value'} always
        def set_json(self, dict_obj):
            try:
                k, v = list(dict_obj.items())[0]
                v = pickle.dumps(v)
                return self.redis_cache.set(k, v)
            except redis.ConnectionError:
                return None

        def get_json(self, key):
            try:
                temp = self.redis_cache.get(key)
                #print(temp)
                if temp:
                    temp= pickle.loads(temp)
                return temp
            except redis.ConnectionError:
                return None
            return None

        def execute_pipe_commands(self, commands):
            #TBD to increase efficiency can chain commands for getting cache in one go
            return None
            
    except:
        pass


#Key Builder
def read_json_file(json_file):
    with open(json_file,'r') as f:
        data = json.load(f)
        f.close()
        return data

def get_workstation_id(json_file):
    workstation_dict = read_json_file(json_file)
    workstation_id = workstation_dict['wid']
    return workstation_id

#data = {
#        "active": True,
#        "_id": "5f3b81e278b0a19d1ec64ab0",
#        "workstation_name": "WS-01",
#        "workstation_ip":'localhost',#"192.168.0.2"
#        "client_port" : '6379',#"6379"
#        "camera_config": {
#            "cameras": [
#                {
#                    "camera_name": "top_camera",
#                    # "camera_id": "Pillar part with SRS CLip Absenece(LH).mp4"
#                    #"camera_id": 'felt.jpg'
#                    "camera_id": 1
#                },
#                {
#                    "camera_name": "kanban_camera",
#                    "camera_id": 0
#                }
#                
#                ]}
#}

def get_workstation_by_id(wid):
    mp = MongoHelper().getCollection("workstations")
    pp = mp.find_one({'_id' : ObjectId(wid)})
    #pp = data
    #print(data)
    return pp


#@singleton    
#class RedisKeyBuilderWorkstation():
#    def __init__(self):
#        self.wid = get_workstation_id('livis//workstation_settings//settings_workstation.json')
#        self.wid = "5f3b81e278b0a19d1ec64ab0"
#        self.workstation_info = data
#    
#    def get_key(self, camera_id, identifier):
#        return "{}_{}_{}".format(self.workstation_info["workstation_name"], str(camera_id), identifier)



class RedisKeyBuilderServer():
    def __init__(self, wid):
        self.workstation_info = get_workstation_by_id(wid)
    
    def get_key(self, camera_id, identifier):
        return "{}_{}_{}".format(self.workstation_info["workstation_name"], str(camera_id), identifier)




def start_toyoda_process(data):
    part_number = data.get('part_number',None)
    user_id = data.get('user_id')
    model_number = data.get('model_number')
    short_number = data.get('short_number')
    part_description = data.get('part_description')
    plan = get_todays_planned_production_util(short_number)
    current_production_count = data.get('current_production_count')
    workstation_id = str(data.get('workstation_id'))
    user_id = data.get('user_id')
    #user_details = get_user_account_util(user_id)
    url = "http://"+SERVER_HOST+":8000/livis/v1/accounts/get_user_account/{}"
    user_details = requests.get(url.format(user_id))
    user_details_json = user_details.json()
    #role_name = user_details['role_name']
    #print("role_name::::",role_name,type(role_name))
    user = { "user_id": user_id,
                "role": user_details_json['role_name'],
                "name": (user_details_json['first_name']+" "+user_details_json['last_name'])
            }
    createdAt = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    mp = MongoHelper().getCollection('inspection_data')
    obj = {
        'part_number' : part_number,
        'user' : user,
        "model_number" : model_number,
        "workstation_id" : workstation_id,
        "short_number" : short_number,
        "part_description" : part_description,
        "plan" : plan,
        "status" : 'started',
        'createdAt' : createdAt,
        'current_production_count' : current_production_count,
        'is_manual' : False,
        'manual_inspection_result' : []
    }
    # set_kanban_on_redis(workstation_id, short_number) 
    _id = mp.insert(obj)
    #workstation_info = RedisKeyBuilderServer(workstation_id).workstation_info
    cc = CacheHelper()
    curr_inspection_key = RedisKeyBuilderServer(workstation_id).get_key(0, 'curr-inspection-id')
    if curr_inspection_key:
        cc.set_json({curr_inspection_key : str(_id)}) 
        resp = mp.find_one({"_id" : _id})
        print("resp:::::::",resp)
        if resp:
            return resp
        else:
            print("Here 1....!!!!!!!!!!!")
            return {}
    else:
        print("Here 2.........!!!!!!!!!!!")
        return {}


def end_toyoda_process(data):
    mp = MongoHelper().getCollection('inspection_data')
    _id = data
    print("nspection id is  =======",_id)
    pr = mp.find_one({"_id" : ObjectId(_id)})
    if pr:
        pr['completedAt'] = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        completedAt = datetime.datetime.strptime(pr['completedAt'], '%Y-%m-%d %H:%M:%S')
        createdAt = datetime.datetime.strptime(pr['createdAt'], '%Y-%m-%d %H:%M:%S')
        duration = completedAt - createdAt
        pr['duration'] = str(duration)
        pr['plan'] = get_todays_planned_production_util(pr['short_number'])
        inspection_attributes = MongoHelper().getCollection(str(_id))
        total_accepted_parts = inspection_attributes.find({"isAccepted" : True}).count()
        total_parts = inspection_attributes.find().count()
        total_rejected_parts = total_parts - total_accepted_parts
        pr['total_accepted_parts'] = total_accepted_parts
        pr['total_rejected_parts'] = total_rejected_parts
        pr['total_parts'] = total_parts
        workstation_id = pr['workstation_id']
        if pr['manual_inspection_result']:
            qc_inspection_count = len(pr['manual_inspection_result'])
        else:
            qc_inspection_count = 0
        rch = CacheHelper()
        production_count = rch.get_json(RedisKeyBuilderServer(workstation_id).get_key(0,'production_count_key'))
        #print("total_accepted_parts::::::::",total_accepted_parts,"::::::production_count::::::::",production_count)
        if qc_inspection_count != 3:  #qc inspection status
            pr['status'] = 'qc_inspection_failed'
        elif int(total_accepted_parts) < int(production_count): #planned production not achieved status
            pr['status'] = 'planned_production_not_achieved'
        else: #process completed status
            pr['status'] = 'completed'
        mp.update({'_id' : pr['_id']}, {'$set' : pr})
        resp = mp.find_one({"_id" : ObjectId(_id)})
        if resp:
            return resp
        else:
            return {}
    else:
        return {}

def get_partInfo(short_number):   
    mp = MongoHelper().getCollection('parts')
    pr = [i for i in mp.find({"short_number" : short_number})]
    resp = {}
    if len(pr) > 0:
        resp = pr[-1]
        obj = get_todays_planned_production_util(short_number)
        if "planned_production_count" in list(obj.keys()):
            planned_production = obj['planned_production_count']
        else:
            planned_production = 0
        resp.update({'planned_production':planned_production})
        return resp
    else:
        return {}


def get_todays_planned_production_util(short_number):
    current_date = str(datetime.date.today())
    mp = MongoHelper().getCollection('plan')
    obj = mp.find_one({"$and" : [{"short_number": short_number}, {"start_time": {"$lte": current_date}}, {"end_time": {"$gte": current_date}}]})
    
    if obj:
        resp = obj
        return resp
    else:
        resp = {"message" : "Today's planned production details not found."}
        return resp


"""def set_kanban_on_redis(workstation_name, short_number):
    cc = CacheHelper()
    kanban_key = RedisKeyBuilderServer(workstation_name).get_key(0, 'kanban')
    cc.set_json({kanban_key : static_kanban[short_number]})"""


def get_toyoda_running_process(worksatation_id):
    mp = MongoHelper().getCollection('inspection_data')
    print("worksatation_id::::::::",worksatation_id,type(worksatation_id))
    prs = mp.find({"$and": 
                [{"$or":
                [{'status' : 'started'},
                {'status' : 'planned_production_not_achieved'},
                {'status' : 'qc_inspection_failed'}]},
                {"workstation_id": str(worksatation_id)}]
                }).sort([( '$natural', -1 )] )
    #print("prs::::::::::::::::::",prs.count())
    if prs.count() > 0:
        pr = prs[0]
        #print("pr::::::::::::::::::",pr)
        plan_update = pr['plan']
        plan_update['planned_production_count'] = pr['current_production_count']
        #print("plan_update:::::::",plan_update)
        pr['plan'] = plan_update
        cc = CacheHelper()
        production_count = pr['current_production_count']
        production_count_key = RedisKeyBuilderServer(worksatation_id).get_key(0, 'production_count_key')
        #print("production_count:::::::",production_count)
        cc.set_json({production_count_key : production_count}) 
        return pr
    else:
        return {}
