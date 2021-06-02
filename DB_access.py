import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["FaceIt"]
statistics_collection = mydb["statistics"]  # conversation_id, username, participant (other), date, number of times per each emotion,
# *total_time*
special_events_collection = mydb["special events"]  # username, event, date, desired_feeling
users_collection = mydb["users"]  # username, key, salt, email



