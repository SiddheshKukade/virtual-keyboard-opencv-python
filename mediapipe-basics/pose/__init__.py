# POSE ESTIMATION
# POSTIONS OF HUMAN BODY MORE THAN 24 FPS AND ENTIRELY ON CPU
import cv2
import time
import mediapipe as mp
VIDEO_LINK = "https://media.istockphoto.com/videos/female-dancer-dancing-on-grass-field-in-waterfront-part-2-of-2-video-id1308518161"
cap  = cv2.VideoCapture(VIDEO_LINK)
print(cap)
print(cap.read())
ptime = 0
mpPose = mp.solutions.pose
pose = mpPose.Pose(static_image_mode=False )
mpDraw = mp.solutions.drawing_utils
while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(src=img ,code= cv2.COLOR_BGR2RGB)
    result = pose.process(imgRGB)
    # print(result.pose_landmarks)
    # has x,y,z and visibility
    if result.pose_landmarks:
        print(result.pose_landmarks)
        mpDraw.draw_landmarks(image=img,landmark_list=result.pose_landmarks ,connections=mpPose.POSE_CONNECTIONS )
        for id , lm in enumerate(result.pose_landmarks.landmark):
            h,w,c = img.shape
            print(id , lm)
            cx,cy = int(lm.x *w) ,int(lm.y*h)
            cv2.circle(img=img ,center= (cx,cy),radius=10 , color=(244,55,65),thickness=cv2.FILLED )

        ctime = time.time()
        if(ctime -ptime ) != 0:
         fps = 1 / (ctime - ptime)
         ptime = ctime
         cv2.putText(img , "FPS =>"+str(int(fps)), (10,30), cv2.FONT_HERSHEY_DUPLEX, 2, (0,0,255) )

    cv2.imshow("Image", img)
    cv2.waitKey(50)  # this is latency of the video
