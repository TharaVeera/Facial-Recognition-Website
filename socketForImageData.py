# -*- coding: utf-8 -*-
"""
Created on Sun Jul 29 13:40:46 2018

@author: 1023191
"""
import socket
import cv2
import pickle
import numpy as np
import struct
import os
from faceArray import faceArray
#import multiprocessing as mp
#import subprocess
#import sys 
import logging


class socketForImageData(object):
    s = None
    
    def __init__(self, s = None):
        self.id = 0
        self.name= ""
        self.confidence = 0
        if s is None: 
            self.s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.s = s
        
        logging.basicConfig(level=logging.DEBUG, filename="message", filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
        self.noPictureTaken = True
    def beginConnection(self):
        #logging.info("NORMAL Facial stuff STARTING")
        #thread = mp.Process(name = 'thread', target = self.executePiScriptToConnect)
        #thread.daemon = True
        #thread.start()
        try:
            #print('Socket created')
            self.HOST = ""# 172.16.31.70 for local 10.0.8.166 for pi
            self.PORT = 4020
            self.s.bind((self.HOST, self.PORT))
            #print('Socket bind complete')

            self.s.listen(10)
            #print('Socket now listening')
        except socket.error as msg:
            print("Couldn't start listening for raspberry pi")
            return False
        try:
            self.executePiScriptToConnect()
        except:
           print("Couldn't execute bash script on Pi")
           return False
        try:
            self.conn, addr = self.s.accept()
        except:
            print("Couldn't accept connection with raspberry pi")
            return False

        self.data = b''
        self.payload_size = struct.calcsize("L")
        #print("payloadsize ",self.payload_size)
        return True
        
    def endConnection(self):
        if self.s is not None:
            print("SOCKET CLOSING")
            try:
                self.s.close()
            except:
                print("Socket could not be closed")
        #count = 0
        
    def executePiScriptToConnect(self): 
        print("Pi script is beginning to execute")
        triggerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        triggerSocket.connect(('172.16.31.79', 5020))
        triggerSocket.close()
        
    def facialDetectionInit(self, img):
        self.face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        
    def facialDetection(self, img, count, face_id):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #fix counter and thing so image is always retuer
        faces = self.face_detector.detectMultiScale(gray, 1.3, 5)
        print("Faces:", faces)
        os.chdir('dataset') #CHANGE THIS LATER TO UPDATE DATASET FOR DEMO
        for(x,y,w,h) in faces:
            count +=1
            cv2.rectangle(img, (x,y), (x+w, y+h), (255, 0, 0), 2)
            cv2.imwrite("User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h, x:x+w])
            if(count >= 15 and self.noPictureTaken == True): 
                os.chdir('..')
                os.chdir('tempImages')
                cv2.imwrite( "customerImage" +  ".jpg", img) #to be displayed when customer is welcomed
                self.noPictureTaken = False
            #cv2.imshow('image', img)
        #streamBytes = self.convertToBytes(img)
        os.chdir('..')
        return count, img

    def facialRecognitionInit(self, img):
        namesArrayObj = faceArray() #CHANGE THIS LATER TO READ FROM DATABASE
        self.nameArray = namesArrayObj.repopArray()
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        #print("current dir:", os.getcwd())
        os.chdir('trainer') #CHANGE THIS ONCE ON LINUX
        #print("current dir:", os.getcwd())
        self.recognizer.read('trainer.yml') #move this out of the function
        os.chdir('..')
        #print("current dir:", os.getcwd())
        self.cascadePath = "haarcascade_frontalface_default.xml"
        self.faceCascade = cv2.CascadeClassifier(self.cascadePath);
        self.font = cv2.FONT_HERSHEY_COMPLEX
        self.id = 0
        self.confidence = 0
        self.name = None
        #self.strConfidence = ""
        self.countReset = 0
        
    
    def facialRecognition(self, count, img): #log this function
        #logging.info("FR STARTING!!!")
        self.countReset +=1
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.faceCascade.detectMultiScale(
            gray, 
            scaleFactor = 1.2,
            minNeighbors = 5,
            #minSize = (int(minW), int(minH)),
            )
        for(x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w, y+h), (255,0 ,0), 2)
            if (count >= 15 and self.noPictureTaken == True):
                print("current dir:", os.getcwd())
                os.chdir('tempImages')
                print("current dir:", os.getcwd())
                cv2.imwrite( "customerImage" +  ".jpg", img) #to be displayed when customer is welcomed
                os.chdir('..')
                print("current dir:", os.getcwd())
                self.noPictureTaken = False
            #FIND THE NAME
            if(self.name is None or self.countReset == 5):
                logging.info("FR find name start")
                id, confidence = self.recognizer.predict(gray[y:y+h, x:x+w])
                print ("ID " + str(id))
                if (confidence < 100): 
                    self.id =int(id)
                    self.name =self.nameArray[id]
                    self.confidence = confidence
                logging.info("FR find name end")
                self.countReset = 0
            #check if conf is less then 100 --> "0" is perf math
            name = self.name
            id = self.id
            confidence = self.confidence
            if (confidence < 100):
                #id = nameArray[id]
                #self.name = self.nameArray[int(id)]
                #self.id = int(id)
                print ("NAME: ", name)
                #self.confidence = round(100 - confidence)
                strConfidence = " {0}%".format(round(100 - confidence))
            else:
                #id = "unknown"
                id  = 0
                name = "Unknown"
                print("NAME: ", self.name)
                #self.confidence = round(100 - confidence)
                strConfidence = " {0}%".format(round(100 - confidence))
            #logging.info("OVERLAY STARTED")
            cv2.putText(img, str(name), (x+5, y-5), self.font, 1, (255, 255, 255), 2)
            cv2.putText(img, str(strConfidence), (x+5, y+h-5), self.font, 1, (255, 255, 0), 1)
            #logging.info("OVERLAY STOPPED")
            #logging.info("FR STOPPING!!!")
            return id, name, img
    
    def convertToBytes(self, img):
        ret, jpeg = cv2.imencode('.jpg', img)
        return jpeg.tobytes()        
    

    def unpackData(self):
        while len(self.data) < self.payload_size:
            print("here")
            self.data += self.conn.recv(4096)
            print(len(self.data))
        packed_msg_size = self.data[:self.payload_size]
        
        self.data = self.data[self.payload_size:]
        msg_size = struct.unpack("L", packed_msg_size)[0]
        
        while len(self.data) < msg_size:
            self.data += self.conn.recv(4096)
        frame_data = self.data[:msg_size]
        self.data = self.data[msg_size:]
        frame=pickle.loads(frame_data)
        
        return frame
    
    def receiveImageDataFD(self, count, face_id):
        frame = self.unpackData()
        if(frame is None):
            return
        if count == 1: 
            self.facialDetectionInit(frame)
        print(frame.size)
        try:
            count, img = self.facialDetection(frame, count, face_id)
            self.frame = img
            #os.chdir("..")
        except:
            pass
        
        #logging.info("NORMAL Facial stuff ENDING")
        return self.convertToBytes(self.frame)


    def receiveImageDataFR(self, count):
        frame = self.unpackData()
        if(frame is None):
            return
        if (count == 1):
            self.facialRecognitionInit(frame)
        try:
            id, name, frame = self.facialRecognition(count, frame)
            self.id = id
            self.name = name
            self.frame = frame
        except:
            pass
        #logging.info("NORMAL Facial stuff ENDING")
        return self.id, self.name, self.convertToBytes(frame)
    
        
        

  
#FIGURE OUT HOW TO CLOSE THE SOCKET
            

            
            
            
    
    