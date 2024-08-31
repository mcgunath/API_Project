import pymongo

# connecting to mongoclient (locally in this case)
myclient = pymongo.MongoClient('mongodb://localhost:27017/')

# delete the entire database
myclient.drop_database('database')

# defining a database
mydb = myclient['database']

# defining a collection
mycol = mydb["customers"]

# defining an row/item in the collection
mydict = { "name": "John", "address": "Highway 37" }

# remove all rows from the collection
mycol.drop()

# inserts the item into the collection (use insert_many for multiples)
mycol.insert_one(mydict)

# for printing all rows in the collection
for item in mycol.find():
    print(item)