import json
import cv2
from pymongo import MongoClient
from bson.json_util import dumps, loads

# Run mongo in docker
# docker run --name mongodb -d -p 27017:27017 -v mongodbdata:/data/db mongo
# docker run --name mongodb -d -p 27017:27017 mongodb
# docker run --name mongodb -d -p 27017:27017 -v c:/data/db:/data/db mongo

client = MongoClient('mongodb://localhost:27017/afm')
db = client["afm"]
db.projects.drop()

serverStatusResult = db.command("serverStatus")

print(serverStatusResult)

project01 = {
"_id" : "1",
"name" : "Project 1",
"author" : "Hlukhau Dzmitry",
"category" : "Advertising",
"sum" : 101
}

project02 = {
"_id" : "2",
"name" : "Project 2",
"author" : "Hlukhau Dzmitry",
"category" : "Advertising",
"sum" : 214
}

project03 = {
"_id" : "3",
"name" : "Project 3",
"author" : "Hlukhau Dzmitry",
"category" : "Book",
"sum" : 143
}

db.projects.insert_one(project01)
db.projects.insert_one(project02)
db.projects.insert_one(project03)

myquery = {"_id": "1"}
newvalues = {"$set": {"name": "Project 01"}}
db.projects.update_one(myquery, newvalues)

myquery = {"_id": "2"}
newvalues = {"$set": {"author": "Vova Hlukhau"}}
db.projects.update_one(myquery, newvalues)

#print "customers" after the update
for x in db.projects.find():
  print(x)

for x in db.projects.find({}, {"category": "Advertising", "name": 1}):
  print(x)

mydoc = db.projects.find().sort("name", -1)
for x in mydoc:
    json_data = dumps(x, indent=2)
    print(json_data)

mydoc = db.projects.find().sort("name", 1)
for x in mydoc:
    for n in x:
        print(n, " = ", x[n])


pipeline = [
    {"$group": {"_id": "$category", "sum": {"$sum": "$sum"}}},
]

print(list(db.projects.aggregate(pipeline)))

myquery = {"author": "Hlukhau Dzmitry"}
db.projects.delete_one(myquery)

img = cv2.imread('left/2.jpg')
print('Image Dimension is', img.shape)
print('Image Height is', img.shape[0])
print('Image Width is', img.shape[1])
print('Number of Channels is', img.shape[2])

# Window name in which image is displayed
window_name = 'image'

# Using cv2.imshow() method
# Displaying the image
cv2.imshow(window_name, img)

# waits for user to press any key
# (this is necessary to avoid Python kernel form crashing)
cv2.waitKey(0)

# closing all open windows
cv2.destroyAllWindows()