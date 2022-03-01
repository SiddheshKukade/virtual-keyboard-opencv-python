import time
import mediapipe as mp
import cv2
from htm import handDetector

ptime = 0
ctime = 0

cap = cv2.VideoCapture(1)
detector = handDetector()

while True:
    sucess, img = cap.read()
    img = detector.find_hands(img=img)
    list = detector.find_position(img)
    if list:
        print(list[0])
    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime

    cv2.putText(img, "FPS =>" + str(int(fps)), (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 255), 5)
    cv2.imshow("Image ", img)
    cv2.waitKey(1)

