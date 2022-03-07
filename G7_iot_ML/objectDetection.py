from multiprocessing import Process,Queue
from . import config
from imageai.Detection import ObjectDetection
from serverConnector import ServerConnector
serverConnector = ServerConnector()
import os
import cv2
import numpy as np
import time

def computer_detect(c_video_to_detect):
    execution_path = os.getcwd()
    path=os.path.join(execution_path, "yolo.h5")
    #model_path = ('yolo.h5')
    #path = os.path.abspath(model_path)
    detector = ObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath(path)
    detector.loadModel()
    custom_object = detector.CustomObjects(person=True, cell_phone=True, book=True, laptop=True)
    while True:
        while c_video_to_detect.empty():
            time.sleep(0.1)
        img_name = 'c_' + time.strftime("%d-%m-%Y %H-%M-%S", time.localtime()) + '.jpg'
        p_time = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())
        n_p = 0
        n_b = 0
        n_cp = 0
        n_lap = 0
        frame = c_video_to_detect.get()
        frame = detector.detectObjectsFromImage(custom_objects=custom_object, input_image=frame, input_type='array',
                                                output_type='array')
        for eachObject in frame:
            if (type(eachObject) != np.ndarray):
                for eachO in eachObject:
                    if eachO['name'] == 'person':
                        n_p += 1
                    elif eachO['name'] == 'cell phone':
                        n_cp += 1
                    elif eachO['name'] == 'book':
                        n_b += 1
                    elif eachO['name'] == 'laptop':
                        n_lap += 1
        if (n_p > 1) or (n_b > 0) or (n_cp > 0) or (n_lap > 0):
            print('-------------------')
            print('Computer:')
            print(p_time)
            if n_p > 0:
                print('Il y a', n_p, 'personnes')
                #cv2.putText(frame, 'No more than one person in front of the screen！', (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
            if n_b > 0:
                print('Il y a', n_b, 'livre')
                #cv2.putText(frame, 'No books！', (10, 10),cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
            if n_cp > 0:
                print('Il y a', n_cp, 'telephone')
                #cv2.putText(frame, 'No telephone！', (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
            if n_lap > 0:
                print('Il y a', n_lap, 'ordinateur')
            print('We save the picture in', img_name)
            cv2.imwrite('./Screenshot/'+img_name, frame[0])
            if p_time == config.TOLERATE_TIME:
                serverConnector.mark_user_as_cheater(serverConnector.get_me()['id'], True)
            print('-------------------')


def cameraHandler(url,c_video_to_detect):
    camera = cv2.VideoCapture(url)
    #loop
    while True:
        flag,frame = camera.read()
        cv2.imshow('Camera_phone', frame)
        if c_video_to_detect.empty():
            c_video_to_detect.put(frame)
        if not flag:
            break
        if ord('q') == cv2.waitKey(1):
            break

    cv2.destroyAllWindows()

    camera.release()


def ObjD(url):
    c_video_to_detect = Queue()
    comp_detect = Process(target = computer_detect,args = (c_video_to_detect,))
    comp_detect.daemon = True
    comp_detect.start()
    cameraHandler(url,c_video_to_detect)
