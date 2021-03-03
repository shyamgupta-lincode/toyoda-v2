from common.utils import *
from django.utils import timezone
from bson import ObjectId
from livis.settings import *
from common.utils import MongoHelper
from bson.json_util import dumps
from bson.objectid import ObjectId

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
            parts_coll = [p for p in mp.find()]
            print(parts_coll)
            total_production_count = total_production_count +len(parts_col)
    return total_production_count

def production_yield_util():
    #call "total_production_util"
    #from inspection get part_id
    #iterate through {part_id}_logs
    ### increment count if isAccepted==True
    #Calculate the %of total_production_accepted/total_production
    total_prod_count = prodcution_yield_util()
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
   # from front end get time range for example: hourly, seconds, minutes
   #from inspection get part id
   #iterate through part_id logs 
   ###increment  count of parts for every minute difference
   #get average according to desired time range hourly, seconds, minutes etc.
   #return average
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
   total_production_count = 0
   mp = MongoHelper().getCollection(PLAN_COLLECTION)
   plan_colls= [p for p in mp.find()]
   total_planned_count = 0
   for plan in plan_colls:
       total_planned_count = total_planned_count + int(plan["planned_production_count"])
   return total_planned_count
