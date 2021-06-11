import socket
import numpy as np
import cv2
from emotion_detector import EmotionDetector
from datetime import datetime
# localIP = ''
# localPort = 5402
# bufferSize = 1000000

class DetectionServer:

    def __init__(self):
        self.localIP = ''
        self.localPort = 5402
        self.bufferSize = 1000000
        self.stop = False
        self.detector = EmotionDetector()
        self.total_checks = 0
        self.total_matches = 0

    def get_emotions(self, db):
        udp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        udp_server_socket.bind((self.localIP, self.localPort))

        print("UDP server up and listening")

        while not self.stop:
            bytes_address_pair = udp_server_socket.recvfrom(self.bufferSize)

            message = bytes_address_pair[0]
            address = bytes_address_pair[1]  # Client IP

            get_time = False
            name_bytes = b""
            time_bytes = b""
            inx = 1
            is_me = False

            if message[0] == ord("Y"):
                is_me = True

            # Y before name for data on me necessary (updated date 6.6)
            for char in message[1:]:
                inx += 1
                # c = char

                if char == ord("\n"): # int value of the char
                    if get_time is True:
                        break
                    get_time = True
                    continue
                if get_time is False:
                    name_bytes += bytes([char])
                else:
                    time_bytes += bytes([char])

            img_bytes = message[inx:]
            name = name_bytes.decode()
            time = time_bytes.decode()
            time = datetime.fromisoformat(time)  # todo insert to DB, only first one, save to variable only first iteration


            np_arr = np.frombuffer(img_bytes, np.uint8)
            img_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)  # cv2.IMREAD_COLOR in OpenCV 3.1

            prediction = self.detector.call(img_np)
            if prediction is not None:
                print(prediction)
                # Sending a reply to client
                udp_server_socket.sendto(str.encode(prediction), address)
            else:
                print("not detected")
                udp_server_socket.sendto(str.encode("not detected"), address)

        udp_server_socket.close()

    def stop_conversation(self, checks, matches):
        self.total_checks = checks
        self.total_matches = matches
        # todo save to DB
        self.stop = True

    def set_stop_false(self):
        self.stop = False

    def get_stop(self):
        return self.stop
