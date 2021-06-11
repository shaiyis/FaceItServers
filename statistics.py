import socket
import numpy as np
import cv2
from flask_pymongo import PyMongo
from datetime import datetime, timedelta


class Statistics:

    def __init__(self, db):
        self.db = db

    def get_user_match(self, user_name, time):
        # self.db_insert_statistics_example()
        now = datetime.now()
        # check last week's conversations
        week_ago = now - timedelta(days=7)
        # check the last month's conversations (last 30 days)
        month_ago = now - timedelta(days=30)
        print(f"week ago: {week_ago}")

        percentage = None
        if time == "last_call":
            print("last_call")
            all_user_matches = self.db.statistics.find(
                {"username": user_name, "is_user": True}, {"matches": 1, "checks": 1}).sort("date", -1)
            if all_user_matches is not None:
                all_user_matches = all_user_matches[:1]
        elif time == "last_week":
            print("last_week")
            all_user_matches = self.db.statistics.find(
                {"username": user_name, "is_user": True, "date": {"$gte": week_ago}})
        elif time == "last_month":
            print("last_month")
            all_user_matches = self.db.statistics.find(
                {"username": user_name, "is_user": True, "date": {"$gte": month_ago}})
        else:
            all_user_matches = None
        if all_user_matches is not None:
            all_checks, all_matches = self.get_checks_and_matches(all_user_matches)
            percentage = round(float(all_matches / all_checks) * 100, 2)

        return percentage

    def get_checks_and_matches(self, all_matches_from_db):
        all_checks, all_matches, i = 0, 0, 0
        for x in all_matches_from_db:
            print(f"item number {i + 1}")
            print(x)
            all_checks += x["checks"]
            all_matches += x["matches"]
            i = i + 1
        return all_checks, all_matches

    def db_insert_statistics_example(self):
        # conversation_id, username, participant (name if not username - user),
        # date, is_user, number of times per each emotion, checks, matches
        mylist = []
        username = "Yossi"

        # גילעד זה מdataset בשם FER2013 ויש שם happy, neutral, sad, angry, surprise, disgust, fear
        for i in range(40):
            mylist.append(
                {"conversation_id": i,
                 "username": username,
                 "participant": "user",
                 "date": datetime.now() - timedelta(days=i % 8),
                 "is_user": True,
                 "happy": i * 10 + 1,
                 "neutral": i * 10 + 2,
                 "sad": i * 10 + 3,
                 "angry": i * 10 + 4,
                 "surprise": i * 10 + 5,
                 "disgust": i * 10 + 6,
                 "fear": i * 10 + 7,
                 "checks": i + 5,
                 "matches": i
                 }
            )
            mylist.append(
                {"conversation_id": i,
                 "username": username,
                 "participant": "Yonatan",
                 "date": datetime.now(),
                 "is_user": False,
                 "happy": i * 10 + 1,
                 "neutral": i * 10 + 2,
                 "sad": i * 10 + 3,
                 "angry": i * 10 + 4,
                 "surprise": i * 10 + 5,
                 "disgust": i * 10 + 6,
                 "fear": i * 10 + 7,
                 "checks": i + 5,
                 "matches": i
                 }
            )

        # mylist = [
        #     {"conversation_id": "123", "participant": "Apple st 652"},
        #     {"name": "Hannah", "address": "Mountain 21"},
        #     {"name": "Michael", "address": "Valley 345"},
        #     {"name": "Sandy", "address": "Ocean blvd 2"},
        #     {"name": "Betty", "address": "Green Grass 1"},
        #     {"name": "Richard", "address": "Sky st 331"},
        #     {"name": "Susan", "address": "One way 98"},
        #     {"name": "Vicky", "address": "Yellow Garden 2"},
        #     {"name": "Ben", "address": "Park Lane 38"},
        #     {"name": "William", "address": "Central st 954"},
        #     {"name": "Chuck", "address": "Main Road 989"},
        #     {"name": "Viola", "address": "Sideway 1633"}
        # ]
        self.db.statistics.insert_many(mylist)


# conversation_id, username, participant (other), date, number of times per each emotion,
# *total_time*
def ticks(dt):
    return (dt - datetime(1, 1, 1)).total_seconds() * 10000000
