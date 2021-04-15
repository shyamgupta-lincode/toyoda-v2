from common.utils import *
from django.utils import timezone
from bson import ObjectId
from livis.settings import *
from common.utils import MongoHelper
from bson.json_util import dumps
from bson.objectid import ObjectId
import datetime
from datetime import datetime, timedelta
import redis
import pickle

def loss_vs_epoch_util(data):
    try:
        exp_id = data['experiment_id']
    except:
        message = "experiment ID not provided"
        status_code= 200
        return message, status_code
    mp = MongoHelper().getCollection('experiment')
    coll = mp.find_one({"_id": ObjectId(exp_id)})
    loss = coll['history']['loss']
    epochs = []
    for i in range(1,len(loss)+1):
        epochs.append(str(i))
    #data = {"epochs": epochs, "loss": loss}
    data = {"x_axis":{"title":"epochs", "categories":epochs},"y_axis":{"title":"loss","value":loss}}
    return data, 200

def reg_loss_vs_epoch_util(data):
    try:
        exp_id = data['experiment_id']
    except:
        message = "experiment ID not provided"
        status_code= 200
        return message, status_code
    mp = MongoHelper().getCollection('experiment')
    coll = mp.find_one({"_id": ObjectId(exp_id)})
    loss = coll['history']['regression_loss']
    epochs = []
    for i in range(1,len(loss)+1):
        epochs.append(str(i))
    #data = {"epochs": epochs, "regression_loss": loss}
    data = {"x_axis":{"title":"epochs", "categories":epochs},"y_axis":{"title":"regression_loss","value":loss}}
    return data, 200

def class_loss_vs_epoch_util(data):
    try:
        exp_id = data['experiment_id']
    except:
        message = "experiment ID not provided"
        status_code= 200
        return message, status_code
    mp = MongoHelper().getCollection('experiment')
    coll = mp.find_one({"_id": ObjectId(exp_id)})
    loss = coll['history']['classification_loss']
    epochs = []
    for i in range(1,len(loss)+1):
        epochs.append(str(i))
    #data = {"epochs": epochs, "classification_loss": loss}
    data = {"x_axis":{"title":"epochs", "categories":epochs},"y_axis":{"title":"classification_loss","value":loss}}
    return data, 200

def map_vs_epoch_util(data):
    try:
        exp_id = data['experiment_id']
    except:
        message = "experiment ID not provided"
        status_code= 200
        return message, status_code
    mp = MongoHelper().getCollection('experiment')
    coll = mp.find_one({"_id": ObjectId(exp_id)})
    map = coll['history']['mAP']
    epochs = []
    for i in range(1,len(map)+1):
        epochs.append(str(i))
    #data = {"epochs": epochs, "mAP": map}
    data = {"x_axis":{"title":"epochs", "categories":epochs},"y_axis":{"title":"mAP","value":map}}
    return data, 200

def lr_vs_epoch_util(data):
    try:
        exp_id = data['experiment_id']
    except:
        message = "experiment ID not provided"
        status_code= 200
        return message, status_code
    mp = MongoHelper().getCollection('experiment')
    coll = mp.find_one({"_id": ObjectId(exp_id)})
    lr = coll['history']['lr']
    lr_format = []
    for i in lr:
        lr_format.append("{:.8f}".format(float(str(i))))
    epochs = []
    for i in range(1,len(lr_format)+1):
        epochs.append(str(i))
    #data = {"epochs": epochs, "lr": lr_format}
    data = {"x_axis":{"title":"epochs", "categories":epochs},"y_axis":{"title":"lr","value":lr_format}}
    return data, 200



def retinanet_training_stats_utils(data):
    try:
        exp_id = data['experiment_id']
    except:
        message = "experiment ID not provided"
        status_code= 200
        return message, status_code

    mp = MongoHelper().getCollection('experiment')
    coll = mp.find_one({"_id": ObjectId(exp_id)}) 
    status = coll["status"] 
    master_dict ={}
    # epochs = []
    # loss = []
    # regression_loss = []
    # classification_loss = []
    # mAp = []

    if status == "Running":
        epochs = []
        loss = []
        regression_loss = []
        classification_loss = []
        mAp = []
        r = redis.Redis(host=REDIS_CLIENT_HOST_AWS,port=REDIS_CLIENT_PORT_AWS,db = 0)
        collection_ = r.get(str(exp_id))
        collection_ = pickle.loads(collection_)
        data_dict = []
        for epoch_number in collection_:
            epochs.append(int(epoch_number))
            data_dict.append(collection_[epoch_number])  

        for i in data_dict:
            loss.append(i["loss"])
            regression_loss.append(i["regression_loss"])
            classification_loss.append(i["classification_loss"])
            mAp.append(i["mAP"])      

        master_dict["loss"] = {"x_axis":{"title":"epochs", "categories":epochs},"y_axis":{"title":"loss","value":loss}}
        master_dict["regression_loss"] = {"x_axis":{"title":"epochs", "categories":epochs},"y_axis":{"title":"regression_loss","value":regression_loss}}
        master_dict["classification_loss"] = {"x_axis":{"title":"epochs", "categories":epochs},"y_axis":{"title":"classification_loss","value":classification_loss}}
        master_dict["mAP"] = {"x_axis":{"title":"epochs", "categories":epochs},"y_axis":{"title":"mAP","value":mAp}}
        

    elif status == "Completed":

        epochs = []
        loss = []
        regression_loss = []
        classification_loss = []
        mAp = []
        log_coll = coll["retinanet_keras_logs"]
        data_dict = []
        for epoch_number in log_coll:
            epochs.append(int(epoch_number))
            data_dict.append(log_coll[epoch_number])    


        for i in data_dict:
            loss.append(i["loss"])
            regression_loss.append(i["regression_loss"])
            classification_loss.append(i["classification_loss"])
            mAp.append(i["mAP"])

        master_dict["loss"] = {"x_axis":{"title":"epochs", "categories":epochs},"y_axis":{"title":"loss","value":loss}}
        master_dict["regression_loss"] = {"x_axis":{"title":"epochs", "categories":epochs},"y_axis":{"title":"regression_loss","value":regression_loss}}
        master_dict["classification_loss"] = {"x_axis":{"title":"epochs", "categories":epochs},"y_axis":{"title":"classification_loss","value":classification_loss}}
        master_dict["mAP"] = {"x_axis":{"title":"epochs", "categories":epochs},"y_axis":{"title":"mAP","value":mAp}}
        
    elif status == "Initialized":
        master_dict = {}

    else:
        master_dict = {}    

        # print(log_coll)
    # print(master_dict)

    # print(epochs)
    # print(data_dict)
   
    data_ = {"data" :master_dict}
    return data_,200



def retinanet_epoch_status_utils(data):
    try:
        exp_id = data['experiment_id']
    except:
        message = "experiment ID not provided"
        status_code= 200
        return message, status_code

    mp = MongoHelper().getCollection('experiment')
    coll = mp.find_one({"_id": ObjectId(exp_id)}) 
    status = coll["status"] 
    master_dict ={}
    # epochs = []
    # loss = []
    # regression_loss = []
    # classification_loss = []
    # mAp = []

    if status == "Running":
        epochs = []
        r = redis.Redis(host=REDIS_CLIENT_HOST_AWS,port=REDIS_CLIENT_PORT_AWS,db = 0)
        collection_ = r.get(str(exp_id))
        collection_ = pickle.loads(collection_)
        # data_dict = []
        for epoch_number in collection_:
            epochs.append(int(epoch_number))
            # data_dict.append(collection_[epoch_number])  

        epoch_status = len(epochs)

    elif status == "Completed":

        epochs = []
        log_coll = coll["retinanet_keras_logs"]
        # data_dict = []
        for epoch_number in log_coll:
            epochs.append(int(epoch_number))
            # data_dict.append(log_coll[epoch_number])  

        epoch_status = len(epochs)


    elif status == "Initialized":
        epoch_status = 0

    else:
        epoch_status = 0    

        # print(log_coll)
    # print(master_dict)

    # print(epochs)
    # print(data_dict)
   
    data_ = {"epoch_status" :epoch_status}
    return data_,200


