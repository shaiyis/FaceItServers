import socket
import uuid

import numpy as np
import cv2
from flask_pymongo import PyMongo
from datetime import datetime, timedelta

from Behaviors import Behaviors


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
            all_user_matches = self.db.statistics.find(
                {"username": user_name, "is_user": True}, {"matches": 1, "checks": 1}).sort("date", -1)
            if all_user_matches is not None:
                all_user_matches = all_user_matches[:1]
        elif time == "last_week":
            all_user_matches = self.db.statistics.find(
                {"username": user_name, "is_user": True, "date": {"$gte": week_ago}})
        elif time == "last_month":
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
        # self.db_insert_statistics_example()
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
                behaviors = record["behaviors"]
                all_positive = behaviors["happy"] + behaviors["surprise"]
                all_but_neutral = behaviors["total"] - behaviors["neutral"]
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
                behaviors = record["behaviors"]
                if name in map_others:
                    map_others[name][0] += (behaviors["happy"] + behaviors["surprise"])
                    map_others[name][1] += (behaviors["total"] - behaviors["neutral"])
                else:
                    map_others[name] = [behaviors["happy"] + behaviors["surprise"],
                                        behaviors["total"] - behaviors["neutral"]]

            for value in map_others.values():
                users_percents.append(round(float(value[0] / value[1]) * 100, 2))
            percentage = round(sum(users_percents) / len(users_percents), 2)

        return percentage

    def compare_happy_sad(self, user_name, time):
        # self.db_insert_statistics_example()
        after_time = None
        week_ago, month_ago = self.get_week_ago_month_ago()

        if time == "last_call":
            all_records = self.db.statistics.find(
                {"username": user_name, "is_user": True}).sort("date", -1)
            if all_records is not None:
                all_records = all_records[:1]
        else:
            if time == "last_week":
                after_time = week_ago
            else:
                after_time = month_ago
            all_records = self.db.statistics.find(
                {"username": user_name, "is_user": True, "date": {"$gte": after_time}})

        if all_records is None:
            return None

        positive = 0
        negative = 0
        all_total = 0
        for record in all_records:
            behaviors = record["behaviors"]
            current_positive = behaviors["happy"] + behaviors["surprise"]
            positive += current_positive
            current_total = behaviors["total"] - behaviors["neutral"]
            all_total += current_total
            negative += (current_total - current_positive)

        print("positive:", positive)
        print("negative:", negative)

        positive_percents = round(float(positive / all_total) * 100, 2)
        negative_percents = round(float(negative / all_total) * 100, 2)

        return {"positive_percents":positive_percents, "negative_percents":negative_percents}

    def get_all_emotions(self, user_name, time):
        # self.db_insert_statistics_example()
        after_time = None
        week_ago, month_ago = self.get_week_ago_month_ago()

        if time == "last_call":
            all_records = self.db.statistics.find(
                {"username": user_name, "is_user": True}).sort("date", -1)
            if all_records is not None:
                all_records = all_records[:1]
        else:
            if time == "last_week":
                after_time = week_ago
            else:
                after_time = month_ago
            all_records = self.db.statistics.find(
                {"username": user_name, "is_user": True, "date": {"$gte": after_time}})

        if all_records is None:
            return None

        happy = 0
        neutral = 0
        sad = 0
        surprise = 0
        angry = 0
        disgust = 0
        fear = 0
        total = 0
        for record in all_records:
            behaviors = record["behaviors"]
            happy += behaviors["happy"]
            neutral += behaviors["neutral"]
            sad += behaviors["sad"]
            surprise += behaviors["surprise"]
            angry += behaviors["angry"]
            disgust += behaviors["disgust"]
            fear += behaviors["fear"]
            total += behaviors["total"]

        happy_percents = round(float(happy / total) * 100, 2)
        neutral_percents = round(float(neutral / total) * 100, 2)
        sad_percents = round(float(sad / total) * 100, 2)
        surprise_percents = round(float(surprise / total) * 100, 2)
        angry_percents = round(float(angry / total) * 100, 2)
        disgust_percents = round(float(disgust / total) * 100, 2)
        fear_percents = round(float(fear / total) * 100, 2)

        return {"happy_percents": happy_percents, "neutral_percents": neutral_percents,
                "sad_percents": sad_percents, "surprise_percents": surprise_percents,
                "angry_percents": angry_percents, "disgust_percents": disgust_percents,
                "fear_percents": fear_percents}

    def get_week_ago_month_ago(self):
        now = datetime.now()
        # check last week's conversations
        week_ago = now - timedelta(days=7)
        # check the last month's conversations (last 30 days)
        month_ago = now - timedelta(days=30)

        return week_ago, month_ago

    def db_insert_statistics_example(self):
        # conversation_id, username, participant (name if not username - user),
        # date, is_user, number of times per each emotion, checks, matches
        mylist = []
        username = "Yossi"

        for i in range(40):
            i10 = 10 * i
            conversation_id = uuid.uuid4()
            b1 = Behaviors(i10 + 1, i10 + 2, i10 + 3, i10 + 4, i10 + 5, i10 + 6, i10 + 7)
            b1.update_total()

            mylist.append(
                {"conversation_id": str(i),
                 "username": username,
                 "participant": "user",
                 "date": datetime.now() - timedelta(days=i % 7),
                 "is_user": True,
                 "behaviors": b1.__dict__,
                 "checks": i + 5,
                 "matches": i
                 }
            )
            b1 = Behaviors(i10 + (i + 20), i10 + 2, i10 + 3, i10 + 4, i10 + 5, i10 + 6, i10 + 7)
            b1.update_total()
            mylist.append(
                {"conversation_id": str(i),
                 "username": username,
                 "participant": "Roni",
                 "date": datetime.now() - timedelta(days=i % 7),
                 "is_user": False,
                 "behaviors": b1.__dict__,
                 "checks": i + 5,
                 "matches": i
                 }
            )
            b1 = Behaviors(i10 + (i + 6), i10 + 2, i10 + 3, i10 + 4, i10 + 5, i10 + 6, i10 + 7)
            b1.update_total()
            mylist.append(
                {"conversation_id": str(i),
                 "username": username,
                 "participant": "Moshe",
                 "date": datetime.now() - timedelta(days=i % 7),
                 "is_user": False,
                 "behaviors": b1.__dict__,
                 "checks": i + 5,
                 "matches": i
                 }
            )
            b1 = Behaviors(i10 + (i + 10), i10 + 2, i10 + 3, i10 + 4, i10 + 5, i10 + 6, i10 + 7)
            b1.update_total()
            mylist.append(
                {"conversation_id": str(i),
                 "username": username,
                 "participant": "Steve",
                 "date": datetime.now() - timedelta(days=i % 7),
                 "is_user": False,
                 "behaviors": b1.__dict__,
                 "checks": i + 5,
                 "matches": i
                 }
            )

        for i in range(40, 50):
            i10 = i * 10
            b2 = Behaviors(i10 + 1, i10 + 2, i10 + 3, i10 + 4, i10 + 5, i10 + 6, i10 + 7)
            b2.update_total()
            mylist.append(
                {"conversation_id": str(i),
                 "username": username,
                 "participant": "user",
                 "date": datetime.now() - timedelta(days=20 + i % 7),
                 "is_user": True,
                 "behaviors": b2.__dict__,
                 "checks": i + 5,
                 "matches": i
                 }
            )
            b2 = Behaviors(i10 + (i + 2), i10 + 2, i10 + 3, i10 + 4, i10 + 5, i10 + 6, i10 + 7)
            b2.update_total()
            mylist.append(
                {"conversation_id": str(i),
                 "username": username,
                 "participant": "Roni",
                 "date": datetime.now() - timedelta(days=20 + i % 7),
                 "is_user": False,
                 "behaviors": b2.__dict__,
                 "checks": i + 5,
                 "matches": i
                 }
            )
            b2 = Behaviors(i10 + (i + 20), i10 + 2, i10 + 3, i10 + 4, i10 + 5, i10 + 6, i10 + 7)
            b2.update_total()
            mylist.append(
                {"conversation_id": str(i),
                 "username": username,
                 "participant": "Charmer",
                 "date": datetime.now() - timedelta(days=20 + i % 7),
                 "is_user": False,
                 "behaviors": b2.__dict__,
                 "checks": i + 5,
                 "matches": i
                 }
            )
            b2 = Behaviors(i10 + (i + 6), i10 + 2, i10 + 3, i10 + 4, i10 + 5, i10 + 6, i10 + 7)
            b2.update_total()
            mylist.append(
                {"conversation_id": str(i),
                 "username": username,
                 "participant": "ABABABABA",
                 "date": datetime.now() - timedelta(days=20 + i % 7),
                 "is_user": False,
                 "behaviors": b2.__dict__,
                 "checks": i + 5,
                 "matches": i
                 }
            )
        b = Behaviors(10, 50, 5, 4, 5, 6, 7)
        b.update_total()
        mylist.append(
            {"conversation_id": "200",
             "username": username,
             "participant": "long_time_ago",
             "date": datetime.now() - timedelta(days=50),
             "is_user": False,
             "behaviors": b.__dict__,
             "checks": 5,
             "matches": 5
             }
        )
        self.db.statistics.insert_many(mylist)


# conversation_id, username, participant (other), date, number of times per each emotion,
# *total_time*
def ticks(dt):
    return (dt - datetime(1, 1, 1)).total_seconds() * 10000000
