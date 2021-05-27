import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["FaceIt"]
statistics_collection = mydb["statistics"]  # username, conversation_id, date, hour, number of times per each emotion
special_events_collection = mydb["special events"]  # username, event, date, desired_feeling
users_collection = mydb["users"]  # username, password, email

print(myclient.list_database_names())
print(mydb.list_collection_names())

#  insert many
# mylist = [
#     {"name": "Amy", "address": "Apple st 652"},
#     {"name": "Viola", "address": "Sideway 1633"}
# ]
# x = mycol.insert_many(mylist)
# print(x.inserted_ids)


