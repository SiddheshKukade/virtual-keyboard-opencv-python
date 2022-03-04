# POSE ESTIMATION
# POSTIONS OF HUMAN BODY MORE THAN 24 FPS AND ENTIRELY ON CPU
import cv2
import time
import mediapipe as mp

class poseDetector():
    def __init__(self, mode=False, smooth_landmarks=True , min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.mode = mode
        self.smooth_landmarks = smooth_landmarks
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(static_image_mode=self.mode ,smooth_landmarks= self.smooth_landmarks , min_detection_confidence=self.min_detection_confidence , min_tracking_confidence=self.min_tracking_confidence )
        self.mpDraw = mp.solutions.drawing_utils

    def findPose(self, img, draw =True):

        imgRGB = cv2.cvtColor(src=img ,code= cv2.COLOR_BGR2RGB)
        self.result = self.pose.process(imgRGB)
        if self.result.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(image=img,landmark_list=self.result.pose_landmarks ,connections=self.mpPose.POSE_CONNECTIONS )
        return img

    def findPositions(self, img , draw=True):
        lmList = []
        if self.result.pose_landmarks:
            for id , lm in enumerate(self.result.pose_landmarks.landmark):
                h,w,c = img.shape
                cx,cy = int(lm.x *w) ,int(lm.y*h)
                lmList.append([id , cx, cy])
                if draw:
                  cv2.circle(img=img ,center= (cx,cy),radius=10 , color=(244,55,65),thickness=cv2.FILLED )
        return lmList


def main():
    VIDEO_LINK = "https://media.istockphoto.com/videos/female-dancer-dancing-on-grass-field-in-waterfront-part-2-of-2-video-id1308518161"
    cap = cv2.VideoCapture(VIDEO_LINK)
    ptime = 0
    detector = poseDetector()
    while True:
        success, img = cap.read()
        img = detector.findPose(img)
        lmlist= detector.findPositions(img=img)
        print("Land mark list",lmlist)
        ctime = time.time()
        if (ctime - ptime) != 0:
          fps = 1 / (ctime - ptime)
          ptime = ctime
          cv2.putText(img, "FPS =>" + str(int(fps)), (10, 30), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 0, 255))

        cv2.imshow("Image", img)
        cv2.waitKey(1)  # this is latency of the video
if __name__ == "__main__":
    main()