# use hand gesture to change the volume of the computer
import cv2
import mediapipe as  mp
import time
import math
import numpy as np
from handTracker import  handDetector
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

####################
wCam , hCam  =1280 ,720
##################

detector = handDetector(detectCon=0.7)
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
ptime =0
while True:
    sucess, img = cap.read()
    img = detector.find_hands(img=img, draw=False)
    list = detector.find_position(img, draw=False)
    if list:
        # for thu,bs id are 4 and 8
        # print(list[0][1], list[0][2])
        x1 ,y1 = (list[4][1], list[4][2])
        x2,y2 = (list[8][1], list[8][2])
        cx,cy = (x1+x2)//2, (y1+y2)//2
        cv2.circle(img=img ,center=(list[4][1], list[4][2]), radius=5 , color=(0,0,255),thickness=10, lineType=cv2.FILLED )
        cv2.circle(img=img ,center=(list[8][1], list[8][2]), radius=5 , color=(0,0,255),thickness=10, lineType=cv2.FILLED )
        cv2.line(img , (list[4][1], list[4][2]),(list[8][1], list[8][2]),  (0,0,255), 3)
        cv2.circle(img=img ,center=(cx,cy), radius=5 , color=(0,0,255),thickness=10, lineType=cv2.FILLED )

######################################################
    # FINDING THE LENGTH OF THE LINE
#####################################################
        length = math.hypot(x2-x1 , y2-y1) # CALCULATING BY PYTHAGORAS THEOREM HYPOTHENEUS
        print(f'Length between the 2 points is {length}')
        if length< 50:
          cv2.circle(img=img, center=(cx, cy), radius=5, color=(247, 146, 146), thickness=10, lineType=cv2.FILLED)
        elif length>200:
            cv2.circle(img=img, center=(cx, cy), radius=5, color=(84, 228, 17), thickness=10, lineType=cv2.FILLED)
######################################
#     CHANGE THE VOLUME BASED ON THE LENGTH
#####################################
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    # volume.GetMute()
    # volume.GetMasterVolumeLevel()
    volume.GetVolumeRange()
    volume.SetMasterVolumeLevel(-20.0, None)






    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime

    cv2.putText(img, "FPS =>" + str(int(fps)), (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 255), 5)
    cv2.imshow("Volume Change Using hand Gestures ", img)
    cv2.waitKey(1)