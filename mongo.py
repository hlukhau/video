from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/afm')
db = client.admin

serverStatusResult = db.command("serverStatus")

print(serverStatusResult)

db = client.business

project01 = {
"_id" : "1",
"name" : "Project 1",
"author" : "Hlukhau Dzmitry",
"category" : "Advertising"
}

project02 = {
"_id" : "2",
"name" : "Project 2",
"author" : "Hlukhau Dzmitry",
"category" : "Advertising"
}

#db.projects.insert_one(project02)

myquery = { "_id": "1" }
newvalues = { "$set": { "name": "Project 01" } }
db.projects.update_one(myquery, newvalues)

myquery = { "_id": "2" }
newvalues = { "$set": { "author": "Vova Hlukhau" } }
db.projects.update_one(myquery, newvalues)

#print "customers" after the update:
for x in db.projects.find():
  print(x)

for x in db.projects.find({}, {"category": "Advertising", "name" : 1}):
  print(x)

mydoc = db.projects.find().sort("name", -1)
for x in mydoc:
  print(x)

mydoc = db.projects.find().sort("name", 1)
for x in mydoc:
  print(x)