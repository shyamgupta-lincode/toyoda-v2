from common.utils import *
from django.utils import timezone
from bson import ObjectId
from livis.settings import *
from common.utils import MongoHelper
from bson.json_util import dumps
from bson.objectid import ObjectId
import datetime

def total_production_by_wid_util(data):
    mp = MongoHelper().getCollection(INSPECTION_COLLECTION)
    try:
        workstation_id = data["workstation_id"]
    except:
        return "workstation id not provided", 400
    if w_id == "":
        objs = [i for i in mp.find()]
    else:
        objs = [i for i in mp.find({"workstation_id":w_id})]
    total_production_count = 0
    for ins in objs:
            inspection_id = str(ins['_id'])
            mp = MongoHelper().getCollection(str(inspection_id)+"_"+"log")
            parts_coll = mp.find().count()
            total_production_count = total_production_count + parts_coll
    return total_production_count, 200

def production_yield_by_wid_util(data):
    try:
        w_id = data['workstation_id']
    except:
        return "workstation id  not provided", 400
    if w_id == "":
        objs = [i for i in mp.find()]
    else:
        objs = [i for i in mp.find({"workstation_id":w_id})]
    total_prod_count, status = total_production_by_wid_util(data)
    total_accepted = 0
    mp = MongoHelper().getCollection(INSPECTION_COLLECTION)
    objs = [i for i in mp.find({"workstation_id":w_id})]
    for ins in objs:
        inspection_id = str(ins['_id'])
        mp = MongoHelper().getCollection(inspection_id+"_log")
        #parts_coll = mp.find({"and":[{"isAccepted":True},{"workstation_id":w_id}]}).count()
        #print(parts_coll)
        parts_coll = mp.find({"isAccepted":True}).count()
        total_accepted = total_accepted + parts_coll
    percent_yield = (total_accepted/total_prod_count)*100
    return percent_yield, 200


def production_rate_util(data):
    try:
        w_id = data['workstation_id']
    except:
        return "workstation id  not provided", 400
    time_period = "secs"
    seconds_count = 0
    doc_count = 0
    mp = MongoHelper().getCollection(INSPECTION_COLLECTION)
    if w_id == "":
        objs = [i for i in mp.find()]
    else:
        objs = [i for i in mp.find({"workstation_id":w_id})]
    for ins in objs:
        inspection_id = str(ins['_id'])
        mp = MongoHelper().getCollection(inspection_id + "_log")
        insp_colls = [p for p in mp.find()]
        for i in insp_colls:
            start_time = i["inference_start_time"]
            end_time = i["inference_end_time"]
            ### Assuming hours is a 12 hour clock
            start_time_dt = datetime.datetime.strptime(start_time,"%Y-%m-%d %H:%M:%S")
            end_time_dt = datetime.datetime.strptime(end_time,"%Y-%m-%d %H:%M:%S")
            time_delta = end_time_dt - start_time_dt
            seconds = time_delta.total_seconds()
            seconds_count = seconds_count + seconds
        doc_count = doc_count + len(insp_colls)
    if doc_count>0:
        avg_rate_secs = int(seconds_count/doc_count)
    else:
        return "workstation id data not found", 400
    ## logic needs to be added if time_period is hours or minutes
    return avg_rate_secs, 200

def defect_count_util(data):
    try:
        w_id = data['workstation_id']
    except:
        return "workstation id  not provided", 400
    total_rejected = 0
    mp = MongoHelper().getCollection(INSPECTION_COLLECTION)
    if w_id == "":
        objs = [i for i in mp.find()]
    else:
        objs = [i for i in mp.find({"workstation_id":w_id})]
    for ins in objs:
        inspection_id = str(ins['_id'])
        mp = MongoHelper().getCollection(inspection_id+"_log")
        parts_coll = [p for p in mp.find({"isAccepted":False})]
        total_rejected = total_rejected + len(parts_coll)
    return total_rejected, 200

def total_vs_planned_util(data):
    try:
        w_id = data['workstation_id']
    except:
        return "workstation id not provided", 400
    try:
        part_id = data['part_id']
    except:
        return "part id not provided", 400
    mp = MongoHelper().getCollection(INSPECTION_COLLECTION)
    if w_id != "" and part_id != "":
        objs = [i for i in mp.find({ "workstation_id": w_id, "part_id": part_id})]
    else:
        objs = [i for i in mp.find()]
    total_production_count = 0
    for ins in objs:
            inspection_id = str(ins['_id'])
            mp = MongoHelper().getCollection(str(inspection_id)+"_"+"log")
            parts_coll = mp.find().count()
            #print("parts_coll "+str(parts_coll)+" inspection_id "+str(inspection_id))
            total_production_count = total_production_count + parts_coll
    mp = MongoHelper().getCollection(PLAN_COLLECTION)
    if part_id != "":
        plan_colls= [p for p in mp.find({"part_id": part_id})]
    else:
        plan_colls= [p for p in mp.find()]
    total_planned_count = 0
    for plan in plan_colls:
        total_planned_count = total_planned_count + int(plan["planned_production_count"])
    total_vs_planned = int(total_production_count/total_planned_count)
    return total_planned_count, 200

def defect_distribution_util(data):
    try:
        w_id = data['workstation_id']
    except:
        return "workstation id  not provided", 400
    defect_count = {}
    mp = MongoHelper().getCollection(INSPECTION_COLLECTION)
    if w_id == "":
        objs = [i for i in mp.find()]
    else:
        objs = [i for i in mp.find({"workstation_id":w_id})]
    for p in objs:
        inspection_id = str(p['_id'])
        mp = MongoHelper().getCollection(inspection_id + "_log")
        parts_coll = [p for p in mp.find({"isAccepted": False})]
        for i in parts_coll:
            for j in i['detections_missed']:
                if j in defect_count:
                    defect_count[j] +=1
                else:
                    defect_count[j] = 1
    return defect_count, 200
