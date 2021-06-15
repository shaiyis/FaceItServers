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

    def get_positive_others(self, user_name, time):
        self.db_insert_statistics_example()
        now = datetime.now()
        # check last week's conversations
        week_ago = now - timedelta(days=7)
        # check the last month's conversations (last 30 days)
        month_ago = now - timedelta(days=30)
        users_percents = []
        percentage = None
        if time == "last_call":
            last = self.db.statistics.find(
                {"username": user_name, "is_user": False}).sort("date", -1)
            if last is None:
                return None
            conversation_id = last[0]["conversation_id"]
            all_others = self.db.statistics.find(
                {"username": user_name, "is_user": False, "conversation_id": conversation_id})
            for record in all_others:
                print(record)
                all_positive = record["happy"] + record["surprise"]
                all_but_neutral = record["total"] - record["neutral"]
                users_percents.append(round(float(all_positive / all_but_neutral) * 100, 2))
            percentage = round(sum(users_percents) / len(users_percents), 2)
        elif time == "last_week" or time == "last_month":
            if time == "last_week":
                after_time = week_ago
            else:
                after_time = month_ago
            map_others = {}

            all_others = self.db.statistics.find(
                {"username": user_name, "is_user": False, "date": {"$gte": after_time}})
            for record in all_others:
                print(record)
                name = record["participant"]
                if name in map_others:
                    map_others[name][0] += (record["happy"] + record["surprise"])
                    map_others[name][1] += (record["total"] - record["neutral"])
                else:
                    map_others[name] = [record["happy"] + record["surprise"], record["total"] - record["neutral"]]

            for value in map_others.values():
                users_percents.append(round(float(value[0] / value[1]) * 100, 2))
            percentage = round(sum(users_percents) / len(users_percents), 2)

        return percentage

    def db_insert_statistics_example(self):
        # conversation_id, username, participant (name if not username - user),
        # date, is_user, number of times per each emotion, checks, matches
        mylist = []
        username = "Yossi"

        # גילעד זה מdataset בשם FER2013 ויש שם happy, neutral, sad, angry, surprise, disgust, fear
        for i in range(40):
            i10 = 10 * i
            mylist.append(
                {"conversation_id": i,
                 "username": username,
                 "participant": "user",
                 "date": datetime.now() - timedelta(days=i % 7),
                 "is_user": True,
                 "happy": i10 + 1,
                 "neutral": i10 + 2,
                 "sad": i10 + 3,
                 "angry": i10 + 4,
                 "surprise": i10 + 5,
                 "disgust": i10 + 6,
                 "fear": i10 + 7,
                 "total": 7 * i10 + 1 + 2 + 3 + 4 + 5 + 6 + 7,
                 "checks": i + 5,
                 "matches": i
                 }
            )
            mylist.append(
                {"conversation_id": i,
                 "username": username,
                 "participant": "Roni",
                 "date": datetime.now() - timedelta(days=i % 7),
                 "is_user": False,
                 "happy": i10 + (i + 20),
                 "neutral": i10 + 2,
                 "sad": i10 + 3,
                 "angry": i10 + 4,
                 "surprise": i10 + 5,
                 "disgust": i10 + 6,
                 "fear": i10 + 7,
                 "total": 7 * i10 + 1 + 2 + 3 + 4 + 5 + 6 + 7,
                 "checks": i + 5,
                 "matches": i
                 }
            )
            mylist.append(
                {"conversation_id": i,
                 "username": username,
                 "participant": "Moshe",
                 "date": datetime.now() - timedelta(days=i % 7),
                 "is_user": False,
                 "happy": i10 + (i + 6),
                 "neutral": i10 + 2,
                 "sad": i10 + 3,
                 "angry": i10 + 4,
                 "surprise": i10 + 5,
                 "disgust": i10 + 6,
                 "fear": i10 + 7,
                 "total": 7 * i10 + 1 + 2 + 3 + 4 + 5 + 6 + 7,
                 "checks": i + 5,
                 "matches": i
                 }
            )
            mylist.append(
                {"conversation_id": i,
                 "username": username,
                 "participant": "Steve",
                 "date": datetime.now() - timedelta(days=i % 7),
                 "is_user": False,
                 "happy": i10 + (i + 10),
                 "neutral": i10 + 2,
                 "sad": i10 + 3,
                 "angry": i10 + 4,
                 "surprise": i10 + 5,
                 "disgust": i10 + 6,
                 "fear": i10 + 7,
                 "total": 7 * i10 + 1 + 2 + 3 + 4 + 5 + 6 + 7,
                 "checks": i + 5,
                 "matches": i
                 }
            )

        for i in range(40, 50):
            i10 = i * 10
            mylist.append(
                {"conversation_id": i,
                 "username": username,
                 "participant": "user",
                 "date": datetime.now() - timedelta(days=20 + i % 7),
                 "is_user": True,
                 "happy": i10 + 1,
                 "neutral": i10 + 2,
                 "sad": i10 + 3,
                 "angry": i10 + 4,
                 "surprise": i10 + 5,
                 "disgust": i10 + 6,
                 "fear": i10 + 7,
                 "total": 7 * i10 + 1 + 2 + 3 + 4 + 5 + 6 + 7,
                 "checks": i + 5,
                 "matches": i
                 }
            )
            mylist.append(
                {"conversation_id": i,
                 "username": username,
                 "participant": "Roni",
                 "date": datetime.now() - timedelta(days=20 + i % 7),
                 "is_user": False,
                 "happy": i10 + (i + 2),
                 "neutral": i10 + 2,
                 "sad": i10 + 3,
                 "angry": i10 + 4,
                 "surprise": i10 + 5,
                 "disgust": i10 + 6,
                 "fear": i10 + 7,
                 "total": 7 * i10 + 1 + 2 + 3 + 4 + 5 + 6 + 7,
                 "checks": i + 5,
                 "matches": i
                 }
            )
            mylist.append(
                {"conversation_id": i,
                 "username": username,
                 "participant": "Charmer",
                 "date": datetime.now() - timedelta(days=20 + i % 7),
                 "is_user": False,
                 "happy": i10 + (i + 20),
                 "neutral": i10 + 2,
                 "sad": i10 + 3,
                 "angry": i10 + 4,
                 "surprise": i10 + 5,
                 "disgust": i10 + 6,
                 "fear": i10 + 7,
                 "total": 7 * i10 + 1 + 2 + 3 + 4 + 5 + 6 + 7,
                 "checks": i + 5,
                 "matches": i
                 }
            )
            mylist.append(
                {"conversation_id": i,
                 "username": username,
                 "participant": "ABABABABA",
                 "date": datetime.now() - timedelta(days=20 + i % 7),
                 "is_user": False,
                 "happy": i10 + (i + 6),
                 "neutral": i10 + 2,
                 "sad": i10 + 3,
                 "angry": i10 + 4,
                 "surprise": i10 + 5,
                 "disgust": i10 + 6,
                 "fear": i10 + 7,
                 "total": 7 * i10 + 1 + 2 + 3 + 4 + 5 + 6 + 7,
                 "checks": i + 5,
                 "matches": i
                 }
            )

        mylist.append(
            {"conversation_id": 200,
             "username": username,
             "participant": "long_time_ago",
             "date": datetime.now() - timedelta(days=50),
             "is_user": False,
             "happy": 10,
             "neutral": 50,
             "sad": 5,
             "angry": 4,
             "surprise": 5,
             "disgust": 6,
             "fear": 7,
             "total": 10 + 50 + 5 + 4 + 5 + 6 + 7,
             "checks": 5,
             "matches": 5
             }
        )
        self.db.statistics.insert_many(mylist)


# conversation_id, username, participant (other), date, number of times per each emotion,
# *total_time*
def ticks(dt):
    return (dt - datetime(1, 1, 1)).total_seconds() * 10000000
