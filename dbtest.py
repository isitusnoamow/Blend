from bson.objectid import ObjectId
import pymongo
from datetime import datetime, timezone
import math
from pymongo.message import query
with open('secret.txt') as f:
    secret = f.read()

client = pymongo.MongoClient(f"{secret}")
db = client['borrow']
listings = db['listings']
users = db['users']

def landl(lat1,long1,lat2,long2, d):
    print(lat1,long1,lat2,long2,d)
    dlat = math.radians(lat1)-math.radians(lat2)
    dlong = math.radians(long1)-math.radians(long2)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlong / 2) ** 2
    c = 2 * a * math.sin(math.sqrt(a))
    
    r = 6371
    dist = c * r
    
    if dist * 1000 > d:
        return False
    else:
        return True

def addlisting(user1,item,price,lendtime,location, image):
    listings.insert_one({
        "user": user1,
        "item": item,
        "price": price,
        "lendtime": lendtime,
        "image": image,
        "time": datetime.now(timezone.utc),
        "user2": "",
        "location": location,
        "active": True
    })

def searchlisting(item,distance,coods):
    queryitems = []
    returneditems = []
    for listing in listings.find({"item": item}):
        if listing["active"]:
            queryitems.append(listing)
    lat2 = coods[0]
    long2 = coods[1]
    for stuff in queryitems:
        lat1 = stuff['location'][0]
        long1 = stuff['location'][1]
        if landl(lat1,long1,lat2,long2,distance):
            print(stuff)
            returneditems.append(stuff)
    
    return returneditems

def deactivatelisting(user2,id):
    listings.update_one({"_id": id}, {"$set": {"active": False,
                                               "user2": user2}})
    
    

def allborrows(user):
    queryitems = []
    for listing in listings.find({"user2": user}):
        queryitems.append(listing)
    return queryitems

def alllent(user):
    queryitems = []
    for listing in listings.find({"user": user}):
        queryitems.append(listing)
    return queryitems

def adduser(user,password,number):
    users.insert_one({
        "user": user,
        "password": password,
        "number": number
    })
