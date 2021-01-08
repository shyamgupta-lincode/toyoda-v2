from common.utils import MongoHelper
from livis.settings import *
from bson import ObjectId
from plan.utils import get_todays_planned_production_util
from common.utils import GetLabelData
import datetime
#######################################################################PART CRUDS#######################################################

def add_logs_util(user_id,operation_type,notes):
    try:
        createdAt = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        mp = MongoHelper().getCollection(LOGS_COLLECTION)
        obj = {
            'user_id' : user_id,
            'operation_type' : operation_type,
            "notes" : notes,
            'created_at' : createdAt,
        }
        _id = mp.insert(obj)   
        # print("insert id:::",_id)
        return _id
    except Exception as e:
        return "Could not add log: "+str(e)


def get_access_log_report_util(data):
    skip = 0
    limit = 10
    from_date = data.get('from_date',None)
    to_date = data.get('to_date',None)
    operator_name = data.get('operator_name',None)
    query = []
    # if from_date is not None and to_date is not None :
    #     query.append({'created_at': {"$gte":from_date,"$lte":to_date}})
    mp = MongoHelper().getCollection(LOGS_COLLECTION)
    # if operator_name is not None :
    #     pr = [i['_id'] for i in mp.find({'user_id': operator_name})]
    # else :
    #     pr = [i['_id'] for i in mp.find()]
    # resp = [p for p in mp.find({"$and" : query}).skip(skip).limit(limit)]
    log_list = []
    resp = mp.find({}).skip(skip).limit(limit)
    # print("query id:::",resp)
    if resp:
        for log in resp:
            # print(log)
            log_list.append(log)
    total = mp.find({}).count()
    logs_info = [{"data":log_list,"total":total}]
    # objs =  mp.find(
    #         {
    #             "$and": query
    #         }
    #         )    
    # print("query id:::",objs)
    return logs_info