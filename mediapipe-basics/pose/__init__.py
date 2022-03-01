# POSE ESTIMATION
# POSTIONS OF HUMAN BODY MORE THAN 24 FPS AND ENTIRELY ON CPU
import cv2
import time
import mediapipe as mp
VIDEO_LINK = "https://vod-progressive.akamaized.net/exp=1646143752~acl=%2Fvimeo-prod-skyfire-std-us%2F01%2F1600%2F18%2F458004666%2F2022697956.mp4~hmac=e0e442eb2257a631350ce4b2547df3757480cb7e847afb8f6622aaa3ded25660/vimeo-prod-skyfire-std-us/01/1600/18/458004666/2022697956.mp4?filename=pexels-allan-mas-5362065.mp4"
cap  = cv2.VideoCapture(VIDEO_LINK)
ptime = 0
ctime = 0

mpPose = mp.solutions.pose
pose = mpPose.Pose(static_image_mode=False )
mpDraw = mp.solutions.drawing_utils
while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img , cv2.COLOR_BGR2RGB)
    result = pose.process(imgRGB)
    print(result.pose_landmarks)
    # has x,y,z and visibility
    if result.pose_landmarks:
        mpDraw.draw_landmarks(image=img,landmark_list=result.pose_landmarks ,connections=mpPose.POSE_CONNECTIONS )
    ctime = time.time()
    if (ctime -ptime ) != 0:
        fps = 1 / (ctime - ptime)
        ptime = ctime
        cv2.putText(img , "FPS =>"+str(int(fps)), (10,30), cv2.FONT_HERSHEY_DUPLEX, 2, (0,0,255) )

    cv2.imshow("Image", img)
    cv2.waitKey(50)  # this is latency of the video
