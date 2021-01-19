from common.utils import MongoHelper
from livis.settings import *
from bson import ObjectId
from plan.utils import get_todays_planned_production_util
from common.utils import GetLabelData
#######################################################################PART CRUDS#######################################################
def add_part_details_task(data):

    try:
        

        part_number = data.get('part_number',None)
        part_description = data.get('part_description',None)

        kanban = data.get('kanban',None)
        createdAt = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        isdeleted = False
        mp = MongoHelper().getCollection(PARTS_COLLECTION)
        collection_obj = {
        
           'part_number' : part_number,
           'part_description' : part_description,
           'isdeleted' : isdeleted,
           'kanban' : kanban,
           'created_at': createdAt
        }
        _id = mp.insert(collection_obj)
        return _id
    except Exception as e:
        return "Could not add part: "+str(e)


def delete_part_task(part_id):
    _id = part_id
    mp = MongoHelper().getCollection(PARTS_COLLECTION)
    p = mp.find_one({'_id' : ObjectId(_id)})
    if p:
        isdeleted = p.get('isdeleted')
        if not isdeleted:
            p['isdeleted'] = True
        mp.update({'_id' : p['_id']}, {'$set' :  p})
        return _id
    else:
        return "Part not found."


def update_part_task(data):

    _id = data.get('_id')
    if _id:
        mp = MongoHelper().getCollection(PARTS_COLLECTION)
        pc = mp.find_one({'_id' : ObjectId(_id)})
        if pc:

            
            part_number = data.get('part_number',None)
            part_description = data.get('part_description',None)
            kanban = data.get('kanban',None)
            

            if part_number:
                pc['part_number'] = part_number

            if part_description:
                pc['part_description'] = part_description

            if kanban:
                pc['kanban'] = kanban
                
            mp.update({'_id' : pc['_id']}, {'$set' :  pc})
        else:
            return {"message" : "Part not found"}
        return _id
    else:
        return {"message" : "Please enter the part ID."}


def get_part_details_task(part_id):
    _id = ObjectId(part_id)
    mp = MongoHelper().getCollection(PARTS_COLLECTION)
    p = mp.find_one({'_id' : _id})
    if p:
        return p
    else:
        return {}


def get_parts_task(skip=0, limit=100):
    mp = MongoHelper().getCollection(PARTS_COLLECTION)
    
    parts = [p for p in mp.find({"$and" : [{"isdeleted": False}, { "isdeleted" : {"$exists" : True}}]}).sort( "$natural", -1 )]

    #parts = [p for p in mp.find({"$and" : [{"isdeleted": False}, { "isdeleted" : {"$exists" : True}}]}).skip(skip).limit(limit)]

    for i in parts:
        data = {}
        part_obj_id = i["_id"]
        mp = MongoHelper().getCollection(str(part_obj_id) + '_experiment')
        i["experiments"] = [i for i in mp.find()]
        info = GetLabelData(part_obj_id).get_metrics()
        i["label_info"] = info
    if parts:
        return parts
    else:
        return []

