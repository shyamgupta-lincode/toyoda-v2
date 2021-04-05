from common.utils import *
from django.utils import timezone
from bson import ObjectId
from livis.settings import *
from common.utils import MongoHelper
from bson.json_util import dumps
from bson.objectid import ObjectId
import datetime
from datetime import datetime, timedelta

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
