import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["FaceIt"]
statistics_collection = mydb["statistics"]
# statistics fields:
# conversation_id, username, participant (name. if username - "user"),
# date, is_user, number of times per each emotion, checks, matches


special_events_collection = mydb["special events"]
# special events fields:
# username, event, date, desired_feeling

users_collection = mydb["users"]
# users fields:
# username, key, salt, email



