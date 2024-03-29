import os
import socket
import uuid

import numpy as np
import cv2
from flask_pymongo import PyMongo
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

from Behaviors import Behaviors


class Statistics:

    def __init__(self, db):
        self.db = db

    def get_user_match(self, user_name, time):
        now = datetime.now()
        # check last week's conversations
        week_ago = now - timedelta(days=7)
        # check the last month's conversations (last 30 days)
        month_ago = now - timedelta(days=30)

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
            if all_user_matches.count() > 0:
                all_checks, all_matches = self.get_checks_and_matches(all_user_matches)
                if all_checks == 0:
                    return -1
                percentage = round(float(all_matches / all_checks) * 100, 2)
            else:  # all_user_matches.count() == 0
                percentage = 0

        return percentage

    def get_checks_and_matches(self, all_matches_from_db):
        all_checks, all_matches, i = 0, 0, 0
        for x in all_matches_from_db:
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
            if last.count() <= 0:
                return 0
            conversation_id = last[0]["conversation_id"]
            all_others = self.db.statistics.find(
                {"username": user_name, "is_user": False, "conversation_id": conversation_id})
            if all_others is None:
                return None
            if all_others.count() <= 0:
                return 0
            for record in all_others:
                behaviors = record["behaviors"]
                all_positive = behaviors["happy"] + behaviors["surprise"]
                all_but_neutral = behaviors["total"] - behaviors["neutral"]
                if all_but_neutral > 0:
                    users_percents.append(round(float(all_positive / all_but_neutral) * 100, 2))
            if len(users_percents) > 0:
                percentage = round(sum(users_percents) / len(users_percents), 2)
            else:
                return 0
        elif time == "last_week" or time == "last_month":
            if time == "last_week":
                after_time = week_ago
            else:
                after_time = month_ago
            map_others = {}

            all_others = self.db.statistics.find(
                {"username": user_name, "is_user": False, "date": {"$gte": after_time}})
            if all_others is None:
                return None
            if all_others.count() <= 0:
                return 0
            for record in all_others:
                name = record["participant"]
                behaviors = record["behaviors"]
                if name in map_others:
                    map_others[name][0] += (behaviors["happy"] + behaviors["surprise"])
                    map_others[name][1] += (behaviors["total"] - behaviors["neutral"])
                else:
                    map_others[name] = [behaviors["happy"] + behaviors["surprise"],
                                        behaviors["total"] - behaviors["neutral"]]

            for value in map_others.values():
                if float(value[1]) == 0.0:
                    continue
                users_percents.append(round(float(value[0] / value[1]) * 100, 2))
            if len(users_percents) > 0:
                percentage = round(sum(users_percents) / len(users_percents), 2)
            else:
                return 0

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
        elif all_records.count() <= 0:
            return {"positive_percents": 0, "negative_percents": 0}
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

        if all_total == 0:
            positive_percents = 0
            negative_percents = 0
        else:
            positive_percents = round(float(positive / all_total) * 100, 2)
            negative_percents = round(float(negative / all_total) * 100, 2)

        return {"positive_percents": positive_percents, "negative_percents": negative_percents}

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

        if all_records.count() <= 0:
            return {"happy_percents": 0, "neutral_percents": 0,
                "sad_percents": 0, "surprise_percents": 0,
                "angry_percents": 0, "disgust_percents": 0,
                "fear_percents": 0}

        happy = 0
        neutral = 0
        sad = 0
        surprise = 0
        angry = 0
        disgust = 0
        fear = 0
        total = 0
        happy_percents = 0
        neutral_percents = 0
        sad_percents = 0
        surprise_percents = 0
        angry_percents = 0
        disgust_percents = 0
        fear_percents = 0
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

        if total > 0:
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
        username = "israel"

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

    def send_email(self, username, image, time):
        user = self.db.users.find_one({"username": username})
        if user is None:
            return "user not exist"
        user_email = user["email"]
        time = str(time).replace("_", " ")

        ImgFileName = f"{username}'s statistics for {time}.jpg"
        From = "face.it.server@gmail.com"
        password = "Faceit64123"
        To = user_email

        msg = MIMEMultipart()

        msg['Subject'] = f"Your statistics for {time}"
        msg['From'] = From
        msg['To'] = To

        text = MIMEText(f"Hello {username}!\n\nThis is your statistics for {time}.\n\nFaceIt Team")
        msg.attach(text)
        image = MIMEImage(image, name=os.path.basename(ImgFileName))

        msg.attach(image)

        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.ehlo()
        s.starttls()
        s.ehlo()

        s.login(From, password)
        s.sendmail(From, To, msg.as_string())
        s.quit()
        return "sent"
