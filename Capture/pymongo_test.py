import pymongo
import datetime
import pprint

print("pymongo version:", pymongo.version)

# import the MongoClient class
from pymongo import MongoClient

# build a new client instance for MongoDB passing
# the string domain and integer port to the host parameters
mongo_client = MongoClient('mongodb', 27017) #-- for MAC
#mongo_client = MongoClient('kafka-network', 27017)

host_info = mongo_client['HOST']
print("\nhost:", host_info)
post1 = {"author": "Mike", "text": "My first blog post!", "tags": ["mongodb", "python", "pymongo"],
         "date": datetime.datetime.utcnow()}
post2 = {"author": "Jack", "text": "My first blog post!", "tags": ["mongodb", "python", "pymongo"],
         "date": datetime.datetime.utcnow()}
post3 = {"author": "Mary", "text": "My first blog post!", "tags": ["mongodb", "python", "pymongo"],
         "date": datetime.datetime.utcnow()}
#db = mongo_client['test-database']
db = mongo_client['names-collection']
posts = db.posts
posts.insert_one(post1).inserted_id
posts.insert_one(post2).inserted_id
posts.insert_one(post3).inserted_id
print(db.list_collection_names())
pprint.pprint(pprint.pprint(posts.find_one({"author": "Jack"})))
#print(posts.find_one({"author": "Jack"}))
pprint.pprint(pprint.pprint(posts.find_one({"author": "Mike"})))
pprint.pprint(pprint.pprint(posts.find_one({"author": "Mary"})))
