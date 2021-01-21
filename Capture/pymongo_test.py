import datetime
import pprint
from pymongo import MongoClient


# class MongoHelper:
#     client = None
#
#     def __init__(self, mongo_host, mongo_port, mongo_db):
#         if not self.client:
#             self.client = MongoClient(host=mongo_host, port=mongo_port)
#         self.db = self.client[mongo_db]
#
#     def getDatabase(self):
#         return self.db
#
#     def getCollection(self, mongo_collection):
#         DB = self.db
#         x = DB.get_collection(mongo_collection)
#         return x[mongo_collection]


# build a new client instance for MongoDB passing
# the string domain and integer port to the host parameters
#-- for MAC and docker-compose where mongodb is the name of the mongo container
# mongo_client = MongoClient('mongodb', 27017)
#
#
# host_info = mongo_client['HOST']
# print("\nhost:", host_info)
# post1 = {"author": "Mike", "text": "My first blog post!", "tags": ["mongodb", "python", "pymongo"],
#          "date": datetime.datetime.utcnow()}
# post2 = {"author": "Jack", "text": "My first blog post!", "tags": ["mongodb", "python", "pymongo"],
#          "date": datetime.datetime.utcnow()}
# post3 = {"author": "Mary", "text": "My first blog post!", "tags": ["mongodb", "python", "pymongo"],
#          "date": datetime.datetime.utcnow()}
# #db = mongo_client['test-database']
# db = mongo_client['names-collection']
# posts = db.posts
# posts.insert_one(post1).inserted_id
# posts.insert_one(post2).inserted_id
# posts.insert_one(post3).inserted_id
# print(db.list_collection_names())
# pprint.pprint(pprint.pprint(posts.find_one({"author": "Jack"})))
# #print(posts.find_one({"author": "Jack"}))
# pprint.pprint(pprint.pprint(posts.find_one({"author": "Mike"})))
# pprint.pprint(pprint.pprint(posts.find_one({"author": "Mary"})))

def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance


MONGO_COLLECTIONS = ["parts-metadata"]
@singleton
class MongoHelper:
    client = None
    def __init__(self):
        if not self.client:
            self.client = MongoClient(host="mongodb", port=27017)
        self.db = self.client["parts-metadata"]

    def getDatabase(self):
        return self.db

    def getCollection(self, cname, create=False, codec_options=None):
        _DB = "parts-metadata"
        DB = self.client[_DB]
        if cname in MONGO_COLLECTIONS:
            if codec_options:
                return DB.get_collection(MONGO_COLLECTIONS[cname], codec_options=codec_options)
            return DB[MONGO_COLLECTIONS[cname]]
        else:
            return DB[cname]


parts_meta_obj = MongoHelper().getCollection("parts-metadata")
for i in parts_meta_obj.find():
    print(i)


