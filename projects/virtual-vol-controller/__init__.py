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
vol =0
volBar =400
volPer = 0
####################
wCam , hCam  =1280 ,720
##################

detector = handDetector(detectCon=0.7)
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
ptime =0

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
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
        elif length>150:
            cv2.circle(img=img, center=(cx, cy), radius=5, color=(84, 228, 17), thickness=10, lineType=cv2.FILLED)



######################################
#     CHANGE THE VOLUME BASED ON THE LENGTH
#####################################

        # volume.GetMute()
        # volume.GetMasterVolumeLevel()
        # volume.SetMasterVolumeLevel(-20.0, None)
        volRange =volume.GetVolumeRange()
        minVol = volRange[0]  # -65.25
        maxVol = volRange[1] # 0

        # print(volume.GetVolumeRange())
        # sample Range :
        # (-65.25, 0.0, 0.03125)
        # -65 - minimum volume
        # 0 - maximun volume

        # HAND RANGE = 50 - 300
        # VOLUME RANGE  = -65- 0
        # print(f'Min {minVol} ||| , {maxVol}')
        # print(f'Min {type(minVol)} ||| , {type(maxVol)}')
        # print(f'Min {type(50.00)} ||| , {type(300)}')

        vol = np.interp(length ,[50.00 , 150.00], [ minVol , maxVol] )
        volBar = np.interp(length ,[50.00 , 150.00], [ 400 , 150] )
        volPer = np.interp(length ,[50.00 , 150.00], [ 0 , 100] )
        # print1
        cv2.putText(img,  str(int(volPer))+"%", (40, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 5)

        volume.SetMasterVolumeLevel(vol,None) # change the volume

    cv2.rectangle(img , (50,150), (85,400 ), (0,255,0), 3)
    cv2.rectangle(img , (50,150), (85,int(volBar)), (255,0, 0 ), 3, cv2.FILLED)
    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime

    cv2.putText(img, "FPS =>" + str(int(fps)), (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 255), 5)
    cv2.imshow("Volume Change Using hand Gestures ", img)
    cv2.waitKey(1)