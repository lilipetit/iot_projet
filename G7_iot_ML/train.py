import cv2
import os
import sys
from PIL import Image
import numpy as np

def getImageAndLabels(path):
    facesSamples=[]
    ids=[]
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)]

    face_detector = cv2.CascadeClassifier('./haarcascades/haarcascade_frontalface_alt_tree.xml')
   
    print('order：',imagePaths)
    imagePaths.remove('./data_img/.DS_Store')
    print('order：', imagePaths)
   
    for imagePath in imagePaths:
        print('nom', imagePath)

        PIL_img=Image.open(imagePath).convert('L')

        #PIL_img = cv2.resize(PIL_img, dsize=(400, 400))
        img_numpy=np.array(PIL_img,'uint8')
        print(img_numpy)

        faces = face_detector.detectMultiScale(img_numpy)

        id = int(os.path.split(imagePath)[1].split('.')[0])
        print('id:', id)

        for x,y,w,h in faces:
            ids.append(id)
            facesSamples.append(img_numpy[y:y+h,x:x+w])

        print('fs:', facesSamples)
        print('id:', id)
        print('fs:', facesSamples[id-1])
    print('fs:', facesSamples)

    return facesSamples,ids


def train():

    path='./data_img/'

    faces,ids=getImageAndLabels(path)
    
    recognizer=cv2.face.LBPHFaceRecognizer_create()
    #recognizer.train(faces,names)#np.array(ids)
    recognizer.train(faces,np.array(ids))
    #save
    recognizer.write('trainer/trainer.yml')
    #save_to_file('names.txt',names)




