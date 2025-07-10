import pymongo
dburl="mongodb+srv://rohithvaddepally:thegymstring@cluster0.nn6v2ug.mongodb.net/"
connection=pymongo.MongoClient(dburl)

projectdb=connection["THE_GYM_BYJOHNSON"]
user_data=projectdb["Users"]
admin_data=projectdb["Admin"]
payment_due=projectdb["payments"]
others=projectdb["others"]


