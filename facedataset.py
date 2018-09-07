
import cv2
import os
#from namearray import *

cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video width and height
cam.set(4, 480)
face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#face_id = input('\n Enter user id and press <return> ==> '

#face_id = getNewCID()
#TristanCID = "C1"
face_id = 1
print(face_id)
print("\n  Initializing face capture. Look at the camera and wait...")
count = 0
while(True):
    ret, img = cam.read()
    #if ret is True:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #else:
        #continue
    faces = face_detector.detectMultiScale(gray, 1.3, 5)
    for(x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
        count +=1
        #make a path to save image
        cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg",gray[y:y+h, x:x+w])
        cv2.imshow('image', img)
    k = cv2.waitKey(100) &0xff
    if k == 27:
        break
    elif count >= 40:
        break

print("\n Exiting program")
cam.release()
cv2.destroyAllWindows

#print("ran right")
