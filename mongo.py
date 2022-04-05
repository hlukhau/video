from pymongo import MongoClient

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


pipeline = [
    {"$group": {"_id": "$category", "sum": {"$sum": "$sum"}}},
]

print(list(db.projects.aggregate(pipeline)))

myquery = { "author": "Hlukhau Dzmitry" }
db.projects.delete_one(myquery)

