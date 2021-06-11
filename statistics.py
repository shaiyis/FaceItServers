import socket
import numpy as np
import cv2
from flask_pymongo import PyMongo


class Statistics:

    def __init__(self, db):
        self.db = db

    def get_user_match(self, user_name, time):
        # self.db_insert_example()
        if time == "last_call":
            print("last_call")
            last_call_matches = self.db.statistics.find(
                {"username": user_name, "is_user": True}, {"matches": 1, "checks": 1}).sort("date", -1)[0]
            print(last_call_matches)
            if last_call_matches is None:
                return None
            else:
                print(last_call_matches)
                percentage = round(float(last_call_matches["matches"] / last_call_matches["checks"]) * 100, 2)
                return percentage
            # return $ matches of last call
        elif time == "last_week":
            print("last_week")
        elif time == "last_month":
            print("last_month")
        else:
            print("nothing")

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
                 "date": i * 4,
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
                 "date": i * 4,
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
