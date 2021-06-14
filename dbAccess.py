import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["FaceIt"]
statistics_collection = mydb["statistics"]
# statistics fields:
# conversation_id, username, participant (name. if username - "user"),
# date, is_user, number of times per each emotion, checks, matches

# todo save one document per participant. conversation_id, date, username - same for all
# checks, matches only for username, number of times per each emotion - in special object, see VS
# make dict from participant to feelings object and save "number of times per each emotion" as one field (object)
# add total as object field

special_events_collection = mydb["special events"]
# special events fields:
# username, event, date, desired_feeling

users_collection = mydb["users"]
# users fields:
# username, key, salt, email



