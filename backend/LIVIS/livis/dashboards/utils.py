from common.utils import *
from django.utils import timezone
from bson import ObjectId
from livis.settings import *
from common.utils import MongoHelper
from bson.json_util import dumps
from bson.objectid import ObjectId
import datetime

def total_production_util():
    #from inspection get part id
    mp = MongoHelper().getCollection(INSPECTION_COLLECTION)
    objs = [i for i in mp.find()]
    ### iterate through {inspection_id}_logs
    ###increment count for every document
    total_production_count = 0
    for ins in objs:
            inspection_id = str(ins['_id'])
            try:
                mp = MongoHelper.getCollection(inspection_id+"_log")
            except:
                continue
            parts_coll = mp.find().count()
            print(parts_coll)
            total_production_count = total_production_count + parts_coll
    return total_production_count

def production_yield_util():
    #call "total_production_util"
    #from inspection get part_id
    #iterate through {part_id}_logs
    ### increment count if isAccepted==True
    #Calculate the %of total_production_accepted/total_production
    total_prod_count = total_production_util()
    total_accepted = 0
    mp = MongoHelper().getCollection(INSPECTION_COLLECTION)
    objs = [i for i in mp.find()]
    for ins in objs:
        inspection_id = str(ins['_id'])
        mp = MongoHelper.getCollection(inspection_id+"_log")
        parts_coll = [p for p in mp.find({"isAccepted":"True"})]
        total_accepted = total_accepted + len(parts_coll)
    percent_yield = (total_accepted/total_prod_count)*100
    return percent_yield


def production_rate_util():
    # get average_time_rate from front end whether secs, min, hours
    # for every inspection_id log collection
    ######for every document
    ######Convert end time to start time to seconds
    ######add to diff_secs counter
    ######Increment doc_count for every iter
    #### average according to time rate (diff_secs_counter)/doc_count
    time_period = "secs"
    seconds_count = 0
    doc_count = 0
    mp = MongoHelper().getCollection(INSPECTION_COLLECTION)
    objs = [i for i in mp.find()]
    for ins in objs:
        inspection_id = str(ins['_id'])
        mp = MongoHelper.getCollection(inspection_id + "_log")
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
    avg_rate_secs = int(seconds_count/doc_count)
    ## logic needs to be added if time_period is hours or minutes
    return 0

def defect_count_util():
    #from inspection get part id
    ### iterate through {part_id}_logs
    ### increment count if isAccepted==False
    # return count
    total_rejected = 0
    mp = MongoHelper().getCollection(INSPECTION_COLLECTION)
    objs = [i for i in mp.find()]
    for ins in objs:
        inspection_id = str(ins['_id'])
        mp = MongoHelper.getCollection(inspection_id+"_log")
        parts_coll = [p for p in mp.find({"isAccepted":"False"})]
        total_rejected = total_rejected + len(parts_coll)
    return total_rejected

def total_vs_planned_util():
    #call "total_production_util" for total_production count
    #access plan collection
    ###increment count of planned_production_count
    # return (total_production_count, planned_production_count)
    total_production_count = total_production_util()
    mp = MongoHelper().getCollection(PLAN_COLLECTION)
    plan_colls= [p for p in mp.find()]
    total_planned_count = 0
    for plan in plan_colls:
        total_planned_count = total_planned_count + int(plan["planned_production_count"])
    return total_planned_count

def defect_distribution():
    defect_count = {}
    mp = MongoHelper().getCollection(INSPECTION_COLLECTION)
    pr = [i for i in mp.find()]
    for p in pr:
        inspection_id = str(p['_id'])
        mp = MongoHelper.getCollection(inspection_id + "_log")
        parts_coll = [p for p in mp.find({"isAccepted": "False"})]
        for i in parts_coll:
            for j in i['detections_missed']:
                if j in defect_count:
                    defect_count[j] +=1
                else:
                    defect_count[j] = 1
    return defect_count
