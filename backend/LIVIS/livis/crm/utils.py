from django.utils import timezone
from common.utils import MongoHelper
from bson.json_util import dumps
from bson.objectid import ObjectId
from common.utils import *
from django.utils import timezone
from bson import ObjectId
from livis.settings import *
import datetime
from datetime import datetime, timedelta

def create_lead_util(data):
    try:
        lead_owner = data['lead_owner']
    except:
        message = "lead owner not provided"
        status_code = 400
        return message, status_code
    try:
        contact_person = data['contact_person']
    except:
        message = "contact person not provided"
        status_code = 400
        return message, status_code
    try:
        company_name = data['company_name']
    except:
        message = "company name not provided"
        status_code = 400
        return message, status_code
    try:
        company_gst = data['company_gst']
    except:
        message = "company gst not provided"
        status_code = 400
        return message, status_code
    try:
        designation = data['designation']
    except:
        message = "designation not provided"
        status_code = 400
        return message, status_code
    try:
        mobile_no = data['mobile_no']
    except:
        message = "mobile number not provided"
        status_code = 400
        return message, status_code
    try:
        email = data['email']
    except:
        message = "email not provided"
        status_code = 400
        return message, status_code
    try:
        alt_email = data['alternate_email']
    except:
        message = "alternate email not provided"
        status_code = 400
        return message, status_code
    try:
        address = data['address']
    except:
        message = "address not provided"
        status_code = 400
        return message, status_code
    try:
        lead_source = data['lead_source']
    except:
        message = "lead source not provided"
        status_code = 400
        return message, status_code
    try:
        notes = data['notes']
    except:
        message = "notes not provided"
        status_code = 400
        return message, status_code

    try:
        status = data['status']
    except:
        message = "status not provided"
        status = 400
        return message, status_code
    try:
       created_by =data['created_by']
    except:
       message = "created_by not provided"
       status = 400
       return message, status_code
    try:
       assigned_to = data['assigned_to']
    except:
       message = "assigned_to not provided"
       status = 400
       return message, status_code
    mp = MongoHelper().getCollection(LEADS_COLLECTION)
    ### Logic to check if kanban exists
    if mp.find_one({"company_gst":company_gst}):
        status_code = 400
        message = "lead already exists"
        return message, status_code

    isdeleted = False
    collection_obj = {
        'lead_owner': lead_owner,
        'contact_person': contact_person,
        'company_name': company_name,
        'company_gst': company_gst,
        'designation': designation,
        'mobile_no': mobile_no,
        'email': email,
        'alt_email': alt_email,
        'address': address,
        'lead_source': lead_source,
        'isdeleted': False,
        'notes': notes,
        'status': status,
        'created_by': created_by,
        'assigned_to': assigned_to}

    _id = mp.insert(collection_obj)
    message = "Added new lead"
    status_code = 200
    return message, status_code

def get_all_leads_util():
    mp = MongoHelper().getCollection(LEADS_COLLECTION)
    leads_list = [p for p in mp.find({"isdeleted":False})]
    if leads_list:
        return leads_list
    else:
        return []

def get_single_lead_util(id):
    lead_id = id
    _id = ObjectId(lead_id)
    mp = MongoHelper().getCollection(LEADS_COLLECTION)
    p = mp.find_one({'_id': _id})
    if p:
        return p
    else:
        return {}

def get_all_leads_by_status_util(status):
    mp = MongoHelper().getCollection(LEADS_COLLECTION)
    print("status is "+str(status))
    leads_list = [p for p in mp.find({"$and":[{"isdeleted":False},{"status": str(status)}]})]
    if leads_list:
        return leads_list
    else:
        return {}

def update_lead_util(data):
    try:
        lead_owner = data['lead_owner']
    except:
        message = "lead owner not provided"
        status_code = 400
        return message, status_code
    try:
        contact_person = data['contact_person']
    except:
        message = "contact person not provided"
        status_code = 400
        return message, status_code
    try:
        company_name = data['company_name']
    except:
        message = "company name not provided"
        status_code = 400
        return message, status_code
    try:
        company_gst = data['company_gst']
    except:
        message = "company gst not provided"
        status_code = 400
        return message, status_code
    try:
        designation = data['designation']
    except:
        message = "designation not provided"
        status_code = 400
        return message, status_code
    try:
        mobile_no = data['mobile_no']
    except:
        message = "mobile number not provided"
        status_code = 400
        return message, status_code
    try:
        email = data['email']
    except:
        message = "email not provided"
        status_code = 400
        return message, status_code
    try:
        alt_email = data['alternate_email']
    except:
        message = "alternate email not provided"
        status_code = 400
        return message, status_code
    try:
        address = data['address']
    except:
        message = "address not provided"
        status_code = 400
        return message, status_code
    try:
        lead_source = data['lead_source']
    except:
        message = "lead source not provided"
        status_code = 400
        return message, status_code
    try:
       lead_id = data['lead_id']
    except:
       message = "lead ID not provided"
       status_code = 400
       return message, status_code
    try:
       notes = data['notes']
    except:
       message = "notes not provided"
       status_code = 400
       return message, status_code

    try:
       status = data['status']
    except:
       message = "status not provided"
       status_code = 400
       return message, status_code

    mp = MongoHelper().getCollection(LEADS_COLLECTION)
    lead = mp.find_one({"_id": ObjectId(lead_id)})
    lead['lead_owner'] = lead_owner
    lead['contact_person'] = contact_person
    lead['company_name'] = company_name
    lead['company_gst'] = company_gst
    lead['designation'] = designation
    lead['mobile_no'] = mobile_no
    lead['email'] = email
    lead['alt_email'] = alt_email
    lead['address'] = address
    lead['lead_source'] = lead_source
    lead['notes'] = notes
    lead['status'] = status
    mp.update({'_id': lead['_id']}, {'$set': lead})

    message = "Success"
    status_code = 200
    return message, status_code

def delete_lead_util(lead_id):
    mp = MongoHelper().getCollection(LEADS_COLLECTION)
    lead = mp.find_one({'_id': ObjectId(lead_id)})
    isdeleted = lead.get('isdeleted')
    if not isdeleted:
        lead['isdeleted'] = True
    mp.update({'_id': lead['_id']}, {'$set': lead})
    message = "Sucess"
    status_code = 200
    return message, status_code

def check_gst_util(company_gst):
    mp = MongoHelper().getCollection(LEADS_COLLECTION)
    lead = mp.find_one({'company_gst': company_gst})
    if not lead:
        message = "absent"
        status_code = 200
        return message, status_code
    elif len(lead) > 0:
        message = "present"
        status_code = 200
        return message, status_code

def create_task_util(data):
    try:
        subject = data['subject']
    except:
        message = "subject not provided"
        status_code = 400
        return message, status_code
    try:
        due_date = data['due_date']
    except:
        message = "due date not provided"
        status_code = 400
        return message, status_code
    try:
        priority = data['priority']
    except:
        message = "priority not provided"
        status_code = 400
        return message, status_code
    try:
        assigned_to = data['assigned_to']
    except:
        message = "assigned to not provided"
        status_code = 400
        return message, status_code
    try:
        lead_id = data['lead_id']
    except:
        message = "lead id not providded"
        status_code = 400
        return message, status_code

    mp = MongoHelper().getCollection(TASKS_COLLECTION)
    ### How to check if task already exists? Unique field
    isdeleted = False
    collection_obj = {
        'subject': subject,
        'due_date': due_date,
        'priority': priority,
        'assigned_to': assigned_to,
        'isdeleted': isdeleted,
        'created_at': timezone.now(),
        'closed_at': '',
        'lead_id': lead_id}

    _id = mp.insert(collection_obj)
    message = "added task"
    status_code = 200
    return message, status_code

def get_all_tasks_util(lead_id):
    print("getting all tasks")
    mp = MongoHelper().getCollection(TASKS_COLLECTION)
    tasks_list = [p for p in mp.find({"$and":[{"isdeleted":False},{"lead_id":lead_id}]})]
    if tasks_list:
        return tasks_list
    else:
        return []

def get_single_task_util(id):
    try:
        task_id = id
    except:
        message = "task ID not provided"
        status_code = 400
        return message, status_code
    _id = ObjectId(task_id)
    mp = MongoHelper().getCollection(TASKS_COLLECTION)
    p = mp.find_one({'_id':_id})
    if p:
        return p
    else:
        return {}

def update_task_util(data):
    try:
        subject = data['subject']
    except:
        message = "subject not provided"
        status_code = 400
        return message, status_code
    try:
        due_date = data['due_date']
    except:
        message = "due date not provided"
        status_code = 400
        return message, status_code
    try:
        priority = data['priority']
    except:
        message = "priority not provided"
        status_code = 400
        return message, status_code
    try:
        assigned_to = data['assigned_to']
    except:
        message = "assigned to not provided"
        status_code = 400
        return message, status_code
    try:
       task_id = data['task_id']
    except:
       message = "task ID not provided"
       status_code = 400
       return message, status_code
    try:
       closed_at = data['closed_id']
    except:
       message = "closed_at not provided"
       status_code = 400
       return message, status_code

    mp = MongoHelper().getCollection(TASKS_COLLECTION)
    task = mp.find_one({'_id': ObjectId(task_id)})
    print(task)
    task['subject'] = subject
    task['due_date'] = due_date
    task['priority'] = priority
    task['assigned_to'] = assigned_to
    task['closed_at'] = closed_at

    mp.update({'_id': task['_id']}, {'$set': task})
    message = "Success"
    status_code = 200
    return message, status_code

def delete_task_util(task_id):
    mp = MongoHelper().getCollection(TASKS_COLLECTION)
    task = mp.find_one({'_id': ObjectId(task_id)})
    isdeleted = task.get('isdeleted')
    if not isdeleted:
        task['isdeleted'] = True
    mp.update({'_id': task['_id']}, {'$set': task})
    message = "Success"
    status_code = 200
    return message, status_code

def sort_tasks_util(lead_id):
    # sort by latest task added
    #lead_id = ObjectId(lead_id)
    mp = MongoHelper().getCollection(TASKS_COLLECTION)
    tasks_list = [p for p in mp.find({"$and":[{"isdeleted":False},{"lead_id":str(lead_id)}]})]
    print(tasks_list)
    sorted_tasks = tasks_list[::-1]
    return sorted_tasks

def create_todo_util(data):
    try:
        task_id = data['task_id']
    except:
        message = "task ID not provided"
        staus_code = 400
        return message, status_code
    try:
        notes = data['notes']
    except:
        message = "notes not provided"
        status_code = 400
        return message, status_code
    try:
        duration = data['duration']
    except:
        message = "duration not provided"
        status_code = 400
        return message, status_code
    collection_obj = {
        "task_id": task_id,
        "notes": notes,
        "duration": duration,
        "isdeleted": False}

    mp = MongoHelper().getCollection(str(task_id)+"_TodoList")
    mp.insert(collection_obj)
    message = "success"
    status_code = 200
    return message, status_code

def get_all_todo_util(task_id):
    todo_list = []
    mp = MongoHelper().getCollection(str(task_id)+"_TodoList")
    todo_list = [p for p in mp.find()]
    return todo_list

def update_todo_util(data):
    try:
        task_id = data['task_id']
    except:
        message = "task ID not provided"
        status_code = 400
        return message, status_code
    try:
        notes = data['notes']
    except:
        message = "notes not provided "
        status_code = 400
        return message, status_code
    try:
        duration = data['duration']
    except:
        message = "duration not provided"
        status_code = 400
        return message, status_code
    try:
        todo_id = data['todo_id']
    except:
        message = "todo not provided"
        status_code = 400
        return message, status_code
    mp = MongoHelper().getCollection(str(task_id)+"_TodoList")
    todo = mp.find_one({'_id': ObjectId(todo_id)})
    todo['notes'] = notes
    todo['duration'] = duration
    mp.update({'_id': todo['_id']}, {'$set': todo})
    message = "success"
    status_code = 200
    return message, status_code

def delete_todo_util(task_id,todo_id):
    mp = MongoHelper().getCollection(str(task_id)+"_TodoList")
    todo = mp.find_one({'_id':ObjectId(todo_id)})
    isdeleted = todo.get('isdeleted')
    if not isdeleted:
        todo['isdeleted'] = True
    mp.update({'_id': todo['_id']}, {'$set': todo})
    message = "Success"
    status_code = 200
    return message, status_code

def update_lead_status_util(data):
    try:
        lead_id = data['lead_id']
    except:
        message = "lead ID not provided"
        status_code = 400
        return message, status_code
    try:
        status = data['status']
    except:
        message = "status not provided"
        status_code = 400
        return message, status_code
    mp = MongoHelper().getCollection(LEADS_COLLECTION)
    lead = mp.find_one({'_id':ObjectId(lead_id)})
    lead['status'] = status
    mp.update({'_id':lead['_id']}, {'$set': lead})
    message = 'Success'
    status_code = 200
    return message, status_code

def create_lead_source_util(data):
    try:
        lead_source = data['lead_source']
    except:
        message = "lead source not provided"
        status_code = 400
        return message, status_code
    mp = MongoHelper().getCollection(LEAD_SOURCE_COLLECTION)
    if mp.find_one({"$and":[{"lead_source":lead_source},{"isdeleted":False}]}):
        status_code = 400
        message = "lead source already exists"
        return message, status_code

    isdeleted = False
    obj = {"lead_source": lead_source, "isdeleted":isdeleted}
    _id = mp.insert(obj)
    status_code = 200
    message = "Added new lead source"
    return message, status_code

def get_all_lead_source_util():
    mp = MongoHelper().getCollection(LEAD_SOURCE_COLLECTION)
    lead_sources = [p for p in mp.find({"isdeleted":False})]
    if lead_sources:
        return lead_sources
    else:
        return []

def get_single_lead_source_util(id):
    mp = MongoHelper().getCollection(LEAD_SOURCE_COLLECTION)
    p = mp.find_one({'_id' : ObjectId(id)})
    if p:
        return p
    else:
        return []

def delete_lead_source_util(id):
    mp = MongoHelper().getCollection(LEAD_SOURCE_COLLECTION)
    p = mp.find_one({'_id' : ObjectId(id)})
    isdeleted = p.get('isdeleted')
    if not isdeleted:
        p['isdeleted'] = True
    mp.update({'_id' : p['_id']}, {'$set' :  p})
    status_code = 200
    message = "Success"
    return message, status_code
