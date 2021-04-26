# ספרינטים בג'ירה
# הרשאות
# US נכונים בג'ירה

import socket

localIP = ''
localPort = 20001
bufferSize = 1024

msgFromServer = "Hello UDP Client"
bytesToSend = str.encode(msgFromServer)

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")

while True:
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

    message = bytesAddressPair[0]
    address = bytesAddressPair[1]

    clientMsg = "Message from Client:{}".format(message)
    clientIP = "Client IP Address:{}".format(address)

    print(clientMsg)
    print(clientIP)

    # send to ML model
    # UDPServerSocket.sendto(bytesToSend, address)
    # get prediction from ML model
    # bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

    # Sending a reply to client
    UDPServerSocket.sendto(bytesToSend, address)
