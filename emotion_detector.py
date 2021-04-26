from paz.applications import HaarCascadeFrontalFace, MiniXceptionFER
import paz.processors as pr
import numpy as np
import cv2
import socket


class EmotionDetector(pr.Processor):
    def __init__(self):
        super(EmotionDetector, self).__init__()
        self.detect = HaarCascadeFrontalFace(draw=False)
        self.crop = pr.CropBoxes2D()
        self.classify = MiniXceptionFER()
        self.draw = pr.DrawBoxes2D(self.classify.class_names)

    def call(self, image):
        boxes2D = self.detect(image)['boxes2D']
        cropped_images = self.crop(image, boxes2D)
        for cropped_image, box2D in zip(cropped_images, boxes2D):
            box2D.class_name = self.classify(cropped_image)['class_name']
            print(box2D.class_name)
        return self.draw(image, boxes2D)


detect = EmotionDetector()
# you can now apply it to an image (numpy array)
image = cv2.imread("images/637546382815275184.jpg")
detect.call(image)
# predictions = detect(np.array(image))
# print(predictions)


# localIP = ''
# localPort = 20001
# bufferSize = 1024
#
# msgFromServer = "prediction:"
# bytesToSend = str.encode(msgFromServer)
#
# UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# UDPServerSocket.bind((localIP, localPort))
#
# print("UDP ML server up and listening")
#
# while True:
#     bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
#
#     message = bytesAddressPair[0]
#     address = bytesAddressPair[1]
#
#     clientMsg = "Message from Client:{}".format(message)
#     clientIP = "Client IP Address:{}".format(address)
#
#     print(clientMsg)
#     print(clientIP)
#
#     # Sending the prediction to client
#     UDPServerSocket.sendto(bytesToSend, address)

