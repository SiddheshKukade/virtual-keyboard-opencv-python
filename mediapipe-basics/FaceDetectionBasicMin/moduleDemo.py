from module import FaceDetector
import time
import cv2

cap = cv2.VideoCapture(0)
ptime = 0
detector = FaceDetector()
while True:
    sucess, img = cap.read()
    print("Before", img)

    img, bboxes = detector.findFaces(img, False)
    print("After", img)

    ctime = time.time()
    if (ctime - ptime) != 0:
        fps = 1 / (ctime - ptime)
        ptime = ctime
        cv2.putText(img, "FPS =>" + str(int(fps)), (10, 30), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 0, 255))

    cv2.imshow('face Detection', img)
    cv2.waitKey(10)


