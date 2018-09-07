
import cv2
import numpy as np
from PIL import Image
import os

#Path for face image database
path = 'dataset'
recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#get the images and label the data

def getImagesAndLabels(path):
    #print (path)
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
    #print(imagePaths)
    faceSamples = []
    ids = []
    for imagePath in imagePaths:
        PIL_img = Image.open(imagePath).convert('L')
        img_numpy = np.array(PIL_img, 'uint8')
        #print (os.path.split(imagePath))
        #print(os.path.split(imagePath)[-1])
        #print(os.path.split(imagePath)[-1].split(".")[1])
        id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = detector.detectMultiScale(img_numpy)
        for (x,y,w,h) in faces:
            faceSamples.append(img_numpy[y:y+h, x:x+w])
            ids.append(id)
    return faceSamples, ids
print("\n Training faces.  Wait...")
faces, ids = getImagesAndLabels(path)
recognizer.train(faces,np.array(ids))

#Save the model into trainer/trainer.yml
recognizer.write(r'trainer\trainer.yml')
#print the number of faces trained and end program
print("\n  {0} faces trained.".format(len(np.unique(ids))))
