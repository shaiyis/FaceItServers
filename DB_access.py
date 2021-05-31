import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["FaceIt"]
statistics_collection = mydb["statistics"]  # username, conversation_id, date, hour, number of times per each emotion
# or probability
special_events_collection = mydb["special events"]  # username, event, date, desired_feeling
users_collection = mydb["users"]  # username, key, salt, email



