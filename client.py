# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 13:56:07 2018

@author: 1023191
"""


import os
import socket
import pickle
import struct
import cv2

cap = cv2.VideoCapture(0)
try:
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect(('172.16.206.22', 4020)) #Change this IP according to the server running the flask app
except:
    print("Socket connection failed")
#Hari's: 172.16.31.60

while True:
    #print("Client is running")
    ret, frame = cap.read()
    data = pickle.dumps(frame)
    clientsocket.sendall(struct.pack("L", len(data)) + data)
