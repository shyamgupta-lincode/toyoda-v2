from django.utils import timezone
from common.utils import MongoHelper
from bson.json_util import dumps
from bson.objectid import ObjectId

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
        'notes': notes}
    _id = mp.insert(collection_obj)
    message = "Added new lead"
    status_code = 200
    return message, status_code

def get_all_leads_util():
    mp = MongoHelper.getCollection(LEADS_COLLECTION)
    tasks_list = [p for p in mp.find({"isdeleted":False})]
    if tasks_list:
        return tasks_list
    else:
        return []

def get_single_lead_util(id):
    try:
        lead_id = id
    except:
        message = "lead ID not provided"
        status_code = 400
        return message, status_code
    _id = ObjectId(lead_id)
    mp = MongoHelper().getCollection(LEADS_COLLECTION)
    p = mp.find_one({'_id': _id})
    if p:
        return p
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
    mp = MongoHelper().getCollection(LEADS_COLLECTION')
    lead = mp.find_one({'lead_id': ObjectId(lead_id))
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

def check_gst_util(comapny_gst):
    mp = MongoHelper().getCollection(LEADS_COLLECTION)
    lead = mp.find_one({'company_gst': company_gst})
    if len(lead) == 0:
        message = "absent"
        status_code = 200
        return message, status_code
    elif len(lead) > 0:
        message = "present"
        status_code = 200
        return message, status_code
