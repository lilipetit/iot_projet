import cv2
import os

import config as config
from serverConnector import ServerConnector
serverConnector = ServerConnector()

import train

train.train()

recogizer=cv2.face.LBPHFaceRecognizer_create()
recogizer.read('trainer/trainer.yml')
names=[]
warningtime = 0
numb = 0


def warning(img,numb):
    cv2.imwrite('./Screenshot/face' + numb, img)
    numb+=1
    if numb == config.TOLERATE_TIME:
        serverConnector.mark_user_as_cheater(serverConnector.get_me()['id'], True)


def face_detect_demo(img):
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    face_detector=cv2.CascadeClassifier('./haarcascades/haarcascade_frontalface_alt2.xml')
    #face=face_detector.detectMultiScale(gray,1.1,5,cv2.CASCADE_SCALE_IMAGE,(100,100),(300,300))
    face=face_detector.detectMultiScale(gray)
    noface=1
    for x,y,w,h in face:
        # noface=0
        cv2.rectangle(img,(x,y),(x+w,y+h),color=(0,0,255),thickness=2)
        cv2.circle(img,center=(x+w//2,y+h//2),radius=w//2,color=(0,255,0),thickness=1)

        ids, confidence = recogizer.predict(gray[y:y + h, x:x + w])
        print('id:',ids,' confidence：', confidence)
        print('confidence ',confidence)
        if confidence > 80:
            global warningtime
            warningtime += 1
            print("warning time=",warningtime)
            if warningtime > 10:
               warning(img)
               warningtime = 0
            cv2.putText(img, 'unkonw', (x + 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
        else:
            print("name is ",names[ids-1])
            cv2.putText(img,str(names[ids-1]), (x + 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
    # if (noface==1):
    #     warningtime += 1
    #     if warningtime > 10:
    #         warning(img)
    #         warningtime = 0
    #         cv2.putText(img, 'unknow', (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
    cv2.imshow('Camera_computer',img)
    #print('bug:',ids)

def name():
    path = './data_img/'
    #names = []
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)]
    print(imagePaths)
    imagePaths.remove('./data_img/.DS_Store')
    for imagePath in imagePaths:
       name = str(os.path.split(imagePath)[1].split('.',2)[1])
       names.append(name)
    return names

def Ident():

    cap = cv2.VideoCapture(0)
    names=name()
    print(names)
    print(names[0])

    while True:
        flag,frame = cap.read()
        if not flag:
            break
        face_detect_demo(frame)
        if ord('q') == cv2.waitKey(10):
            break

    cv2.destroyAllWindows()

    cap.release()
    print(names)

if __name__ == "__main__":
    Ident()
