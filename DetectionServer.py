import socket
import numpy as np
import cv2
from emotion_detector import EmotionDetector


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

    def get_emotions(self):
        udp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        udp_server_socket.bind((self.localIP, self.localPort))

        print("UDP server up and listening")

        while not self.stop:
            bytesAddressPair = udp_server_socket.recvfrom(self.bufferSize)

            message = bytesAddressPair[0]
            address = bytesAddressPair[1]  # Client IP

            get_time = False
            name_bytes = b""
            time_bytes = b""
            inx = 0

            # Y/N before name for data on me or not - not necessary
            for char in message:
                inx += 1
                c = char
                # \n
                if c == 10:
                    if get_time is True:
                        break
                    get_time = True
                    continue
                if get_time is False:
                    name_bytes += bytes([c])
                else:
                    time_bytes += bytes([c])

            img_bytes = message[inx:]
            name = name_bytes.decode()
            time = time_bytes.decode()

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
        self.stop = True

    def set_stop_false(self):
        self.stop = False

    def get_stop(self):
        return self.stop
