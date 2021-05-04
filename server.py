import socket
import numpy as np
import cv2
from emotion_detector import EmotionDetector

localIP = ''
localPort = 5402
bufferSize = 1000000

# msgFromServer = "Hello UDP Client"
# bytesToSend = str.encode(msgFromServer)

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")
detect = EmotionDetector()

while True:
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

    message = bytesAddressPair[0]
    address = bytesAddressPair[1]  # Client IP

    get_time = False
    name_bytes = b""
    time_bytes = b""
    inx = 0

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

    prediction = detect.call(img_np)
    if prediction is not None:
        print(prediction)
        # Sending a reply to client
        UDPServerSocket.sendto(str.encode(prediction), address)


