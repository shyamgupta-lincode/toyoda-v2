from common.utils import *
from django.utils import timezone
from bson import ObjectId
from livis.settings import *
from common.utils import MongoHelper
from bson.json_util import dumps
from bson.objectid import ObjectId
import datetime
from datetime import datetime, timedelta

def total_production_by_wid_util(data):
    mp = MongoHelper().getCollection(INSPECTION_COLLECTION)
    try:
        w_id = data["workstation_id"]
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
    mp = MongoHelper().getCollection(INSPECTION_COLLECTION)
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
            start_time_dt = datetime.strptime(start_time,"%Y-%m-%d %H:%M:%S")
            end_time_dt = datetime.strptime(end_time,"%Y-%m-%d %H:%M:%S")
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

def production_weekly_util(data):
    try:
        w_id = data['workstation_id']
    except:
        return "workstation id not provided", 400
    try:
        operator_id = data['operator_id']
    except:
        return "operator id not provided", 400
    mp = MongoHelper().getCollection(INSPECTION_COLLECTION)
    if w_id == "" and operator_id=="":
        objs = [i for i in mp.find()]
    elif w_id != "":
        objs = [i for i in mp.find({"workstation_id":w_id})]
    elif operator_id != "":
        objs = [i for i in mp.find({"operator_id":operator_id})]
    date_format = "%Y-%m-%d %H:%M:%S"
    now = datetime.now().replace(microsecond=0)
    #now = datetime(2021, 3, 5, 16, 31, 2)
    toi_end = datetime.strptime(str(now), date_format)
    prev = now - timedelta(days = 7)
    toi_start = datetime.strptime(str(prev), date_format)
    parts = {"1":0,"2":0,"3":0,"4":0,"5":0,"6":0,"7":0,"0":0}
    for ins in objs:
        inspection_id = str(ins['_id'])
        mp = MongoHelper().getCollection(inspection_id + "_log")
        insp_colls = [p for p in mp.find({"isAccepted":True})]
        for i in insp_colls:
            start_time = i["inference_start_time"]
            start_time = datetime.strptime(start_time, date_format)
            end_time = i["inference_end_time"]
            end_time = datetime.strptime(end_time, date_format)
            print("toi_start "+str(toi_start))
            print("toi_end "+str(toi_end))
            print("end time"+str(end_time))
            if end_time >= toi_start and end_time < toi_end:
                time_delta = abs(toi_end - end_time)
                days = time_delta.days
                parts[str(days)] = parts[str(days)] + 1
    print(parts)
    defects = {"1":0,"2":0,"3":0,"4":0,"5":0,"6":0,"7":0,"0":0}
    for ins in objs:
        inspection_id = str(ins['_id'])
        mp = MongoHelper().getCollection(inspection_id + "_log")
        insp_colls = [p for p in mp.find({"isAccepted":False})]
        for i in insp_colls:
            start_time = i["inference_start_time"]
            start_time = datetime.strptime(start_time, date_format)
            end_time = i["inference_end_time"]
            end_time = datetime.strptime(end_time, date_format)
            if end_time >= toi_start and end_time < toi_end:
                time_delta = abs(toi_end - end_time)
                days = time_delta.days
                defects[str(days)] = defects[str(days)] + 1
    print(defects)
    parts_list = []
    for key, value in parts.items():
        if value ==0:
            value = None
        parts_list.append(value)
    defect_list = []
    for key, value in defects.items():
        if value ==0:
            value = None
        defect_list.append(value)
    data = [{"name":"Accepted", "data":parts_list},{"name":"Rejected", "data":defect_list}]
    return data, 200

def production_by_role_util(data):
    try:
        w_id_list = data['workstation_id_list']
    except:
        return "workstation id list  not provided", 400
    try:
        duration = data['duration']
    except:
        return "duration not provided", 400
    try:
        operator_id_list = data['operator_id_list']
    except:
        return "operator ID list not provided", 400
    response = []
    if operator_id_list == []:
        for _id in w_id_list:
            data_wid = {"workstation_id":_id, "operator_id":""}
            if duration.find("weekly") != -1:
                result, status_code = production_weekly_util(data_wid)
            if duration.find("hourly") != -1:
                result, status_code = production_hourly_util(data_wid)
            if duration.find("monthly") != -1:
                result, status_code = production_monthly_util(data_wid)
            response.append({"w_id":_id, "data":result})
    if w_id_list == []:
        for _id in operator_id_list:
            data_opid = {"workstation_id":"","operator_id":_id}
            if duration.find("weekly") != -1:
                result, status_code = production_weekly_util(data_opid)
            if duration.find("hourly") != -1:
                result, status_code = production_hourly_util(data_opid)
            if duration.find("monthly") != -1:
                result, status_code = production_monthly_util(data_opid)
            response.append({"operator_id":_id, "data":result})
    return response, 200

def production_hourly_util(data):
    try:
        w_id = data['workstation_id']
    except:
        return "workstation id not provided", 400
    try:
        operator_id = data['operator_id']
    except:
        return "operator id not provided", 400
    mp = MongoHelper().getCollection(INSPECTION_COLLECTION)
    if w_id == "" and operator_id == "":
        objs = [i for i in mp.find()]
    elif w_id != "":
        objs = [i for i in mp.find({"workstation_id":w_id})]
    elif operator_id != "":
        objs = [i for i in mp.find({"operator_id":operator_id})]
    date_format = "%Y-%m-%d %H:%M:%S"
    now = datetime.now().replace(microsecond=0)
    toi_end = datetime.strptime(str(now), date_format)
    prev = now - timedelta(days = 1)
    toi_start = datetime.strptime(str(prev), date_format)
    parts = {"0":0,"1":0,"2":0,"3":0,"4":0,"5":0,"6":0,"7":0}
    for ins in objs:
        inspection_id = str(ins['_id'])
        mp = MongoHelper().getCollection(inspection_id + "_log")
        insp_colls = [p for p in mp.find({"isAccepted":True})]
        for i in insp_colls:
            start_time = i["inference_start_time"]
            start_time = datetime.strptime(start_time, date_format)
            end_time = i["inference_end_time"]
            end_time = datetime.strptime(end_time, date_format)
            if end_time >= toi_start and end_time < toi_end:
                time_delta = abs(toi_end - end_time)
                hours_ = int(time_delta.total_seconds() / 3600)
                key_ = int(hours_ / 3)
                parts[str(key_)] = parts[str(key_)] + 1
    print(parts)
    defects = {"1":0,"2":0,"3":0,"4":0,"5":0,"6":0,"7":0}

    for ins in objs:
        inspection_id = str(ins['_id'])
        mp = MongoHelper().getCollection(inspection_id + "_log")
        insp_colls = [p for p in mp.find({"isAccepted":False})]
        for i in insp_colls:
            start_time = i["inference_start_time"]
            start_time = datetime.strptime(start_time, date_format)
            end_time = i["inference_end_time"]
            end_time = datetime.strptime(end_time, date_format)
            if end_time >= toi_start and end_time < toi_end:
                time_delta = abs(toi_end - end_time)
                hours_ = int(time_delta.total_seconds() / 3600)
                key_ = int(hours_ / 3)
                defects[str(key_)] = defects[str(key_)] + 1
    print(defects)
    parts_list = []
    for key, value in parts.items():
        if value ==0:
            value = None
        parts_list.append(value)
    defect_list = []
    for key, value in defects.items():
        if value ==0:
            value = None
        defect_list.append(value)
    data = [{"name":"Accepted", "data":parts_list},{"name":"Rejected", "data":defect_list}]
    return data, 200

def production_monthly_util(data):
    try:
        w_id = data['workstation_id']
    except:
        return "workstation id not provided", 400
    try:
        operator_id = data['operator_id']
    except:
        return "operator id not provided", 400
    mp = MongoHelper().getCollection(INSPECTION_COLLECTION)
    if w_id == "" and operator_id == "":
        objs = [i for i in mp.find()]
    elif w_id !="":
        objs = [i for i in mp.find({"workstation_id":w_id})]
    elif operator_id != "":
        objs = [i for i in mp.find({"operator_id":operator_id})]
    date_format = "%Y-%m-%d %H:%M:%S"
    now = datetime.now().replace(microsecond=0)
    toi_end = datetime.strptime(str(now), date_format)
    prev = now - timedelta(days = 365)
    toi_start = datetime.strptime(str(prev), date_format)
    parts = {"0":0, "1":0, "2":0, "3":0, "4":0, "5":0, "6":0, "7":0, "8":0, "9":0, "10":0, "11":0}
    for ins in objs:
        inspection_id = str(ins['_id'])
        mp = MongoHelper().getCollection(inspection_id + "_log")
        insp_colls = [p for p in mp.find({"isAccepted":True})]
        for i in insp_colls:
            start_time = i["inference_start_time"]
            start_time = datetime.strptime(start_time, date_format)
            end_time = i["inference_end_time"]
            end_time = datetime.strptime(end_time, date_format)
            if end_time >= toi_start and end_time < toi_end:
                time_delta = abs(toi_end - end_time)
                days_ = int(time_delta.days / 30)
                print("days diff "+str(days_))
                parts[str(days_)] = parts[str(days_)] + 1
    print(parts)
    defects = {"0":0,"1":0,"2":0,"3":0,"4":0,"5":0,"6":0,"7":0, "8":0, "9":0, "10":0, "11":0}
    for ins in objs:
         inspection_id = str(ins['_id'])
         mp = MongoHelper().getCollection(inspection_id + "_log")
         insp_colls = [p for p in mp.find({"isAccepted":False})]
         for i in insp_colls:
             start_time = i["inference_start_time"]
             start_time = datetime.strptime(start_time, date_format)
             print("start time after parsing "+str(start_time))
             end_time = i["inference_end_time"]
             end_time = datetime.strptime(end_time, date_format)
             if end_time >= toi_start and end_time < toi_end:
                 time_delta = abs(toi_end - end_time)
                 hours_ = int(time_delta.days / 30)
                 print("days diff "+str(days_))
                 defects[str(days_)] = defects[str(days_)] + 1
    print(defects)
    parts_list = []
    for key, value in parts.items():
        if value ==0:
            value = None
        parts_list.append(value)
    defect_list = []
    for key, value in defects.items():
        if value ==0:
            value = None
        defect_list.append(value)
    data = [{"name":"Accepted", "data":parts_list},{"name":"Rejected", "data":defect_list}]
    return data, 200


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
