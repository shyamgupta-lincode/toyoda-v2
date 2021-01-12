from common.utils import MongoHelper
from livis.settings import *
from bson import ObjectId
import datetime
import base64

def add_assects_util(data):

    side_nav = data.get('side_nav',None)
    login_logo = data.get('login_logo',None)
    
    mp = MongoHelper().getCollection(ASSECTS_COLLECTION)
    
    if side_nav is None:
        return "side nav logo not provided",400
    if login_logo is None:
        return "login logo not provided",400
    
    side_nav = str.encode(side_nav)
    login_logo = str.encode(login_logo)
    
    sidenav_img = TRAIN_DATA_STATIC + "/side.png"
    login_img = TRAIN_DATA_STATIC + "/main.png"
    
    side_nav_pth = "http://0.0.0.0:3306/side.png"
    login_img_pth = "http://0.0.0.0:3306/main.png"
    
    with open(sidenav_img, "wb") as fh:
        fh.write(base64.decodebytes(side_nav))

    with open(login_img, "wb") as fh:
        fh.write(base64.decodebytes(login_logo)) 
        
    p = [i for i in mp.find()]
    
    if len(p) == 0:
   
        collection_obj = {
            'side_nav':side_nav_pth,
            'login_img':login_img_pth,
        }

        _id = mp.insert(collection_obj)
        
        p = mp.find_one({'_id' : _id})
        
        return p,200
        
    else:
   
        _id = p[0]['_id']
        dataset = mp.find_one({'_id' : ObjectId(_id)})
    
        collection_obj = {
                'side_nav':side_nav_pth,
                'login_img':login_img_pth,
            }

        mp.update({'_id' : ObjectId(dataset['_id'])}, {'$set' :  collection_obj})
        
        p = mp.find_one({'_id' : _id})
        
        return p,200
    
    


def update_assect_util(data):

    side_nav = data.get('side_nav',None)
    login_logo = data.get('login_logo',None)
    
    mp = MongoHelper().getCollection(ASSECTS_COLLECTION)
        
    sidenav_img = TRAIN_DATA_STATIC + "/side.png"
    login_img = TRAIN_DATA_STATIC + "/main.png"
    
    side_nav_pth = "http://0.0.0.0:3306/side.png"
    login_img_pth = "http://0.0.0.0:3306/main.png"
    
    if side_nav is not None:
        side_nav = str.encode(side_nav)
        with open(sidenav_img, "wb") as fh:
            fh.write(base64.decodebytes(side_nav))
            
    if login_img_pth is not None:
        login_logo = str.encode(login_logo)
        with open(login_img, "wb") as fh:
            fh.write(base64.decodebytes(login_logo)) 
        
    p = [i for i in mp.find()]
    
   
    _id = p[0]['_id']
    dataset = mp.find_one({'_id' : ObjectId(_id)})
    
    collection_obj = {
                'side_nav':side_nav_pth,
                'login_img':login_img_pth,
        }

    mp.update({'_id' : ObjectId(dataset['_id'])}, {'$set' :  collection_obj})
        
    p = mp.find_one({'_id' : _id})
        
    return p,200

