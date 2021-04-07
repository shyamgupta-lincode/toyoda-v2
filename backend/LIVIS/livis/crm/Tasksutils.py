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

def get_tasks_by_user_util(user):
    mp = MongoHelper().getCollection(TASKS_COLLECTION)
    colls = [p for p in mp.find({"assigned_to": user})]
    if colls:
        return colls
    else:
        return []