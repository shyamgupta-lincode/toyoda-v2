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

