import socket
import numpy as np
import cv2
from EmotionDetector import EmotionDetector
from datetime import datetime
from Behaviors import Behaviors


class DetectionServer:

    def __init__(self):
        self.localIP = ''
        self.localPort = 5402
        self.bufferSize = 1000000
        self.stop = False
        self.detector = EmotionDetector()
        self.dbSaver = None

    def get_emotions(self, db_saver):
        self.dbSaver = db_saver
        udp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        udp_server_socket.bind((self.localIP, self.localPort))

        print("UDP server up and listening")

        first_iteration = True

        while not self.stop:
            bytes_address_pair = udp_server_socket.recvfrom(self.bufferSize)

            message = bytes_address_pair[0]
            address = bytes_address_pair[1]  # Client IP

            get_time = False
            participant_bytes = b""
            time_bytes = b""
            inx = 0
            is_me = False

            if message[0] == ord("Y"):
                is_me = True

            # Y before name for data on me necessary (updated date 6.6)
            for char in message:
                inx += 1
                # c = char

                if char == ord("\n"):  # int value of the char
                    if get_time is True:
                        break
                    get_time = True
                    continue
                if get_time is False:
                    participant_bytes += bytes([char])
                else:
                    time_bytes += bytes([char])

            img_bytes = message[inx:]
            participant = participant_bytes.decode()
            if is_me:
                participant = participant[1:]
            date = time_bytes.decode()
            date = datetime.fromisoformat(
                date)

            if participant not in self.dbSaver.feelings_dict:
                if is_me:
                    self.dbSaver.feelings_dict[participant] = [Behaviors(), True]
                else:
                    self.dbSaver.feelings_dict[participant] = [Behaviors(), False]

            if first_iteration:
                self.dbSaver.date = date
                first_iteration = False

            np_arr = np.frombuffer(img_bytes, np.uint8)
            img_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)  # cv2.IMREAD_COLOR in OpenCV 3.1

            prediction = self.detector.call(img_np)
            if prediction is not None:
                print(prediction)
                behaviors = self.dbSaver.feelings_dict[participant][0]
                behaviors.update_behaviors(prediction)
                # Sending a reply to client
                udp_server_socket.sendto(str.encode(prediction), address)
            else:
                print("not detected")
                udp_server_socket.sendto(str.encode("not detected"), address)

        print("thread is here")
        udp_server_socket.close()

    def stop_conversation(self, checks, matches):
        self.dbSaver.total_checks = checks
        self.dbSaver.total_matches = matches
        self.stop = True
        # for loop on feelings_dict and update "total" field
        for participant in self.dbSaver.feelings_dict:
            self.dbSaver.feelings_dict[participant][0].update_total()
        self.dbSaver.save_statistics()

    def set_stop_false(self):
        self.stop = False

    def get_stop(self):
        return self.stop
