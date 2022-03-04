import time

import cv2
import mediapipe as mp


class handDetector():
    def __init__(self,mode=False, maxNoOfHands=2 , detectCon =0.5 ,trackCon = 0.5):
        self.mode = mode
        self.maxNoOfHands = maxNoOfHands
        self.detectCon = detectCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=self.mode , max_num_hands=self.maxNoOfHands,min_tracking_confidence=self.trackCon,min_detection_confidence= self.detectCon)
        self.mpDraw = mp.solutions.drawing_utils

    def find_hands(self, img,draw=True):
        imageRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imageRGB)  # every time hands obj will try to find hands and store them in 'results'
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:  # the co-ordinates can be of multiple hands hence we are
                # using a for loop to get co-ordinated of only singele hand one by one
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,self.mpHands.HAND_CONNECTIONS)  # we are not using imgRGB becuse we are not displaying that image on screen we are displaying our original BGR image
        return img
# not need to draw lines
    def find_position(self, img , handNo=0 , draw=True): # provides the co-oridnates of a single hand part speificed by the input no
        lms  = []
        if self.results.multi_hand_landmarks:
            myHand =  self.results.multi_hand_landmarks[handNo] # we just got all the co-ordinates  of our hand
            # but problem is we just have the ratio of them right now so we need to convert them into actual width and height

            for id ,lm in enumerate(myHand.landmark):
                h,w,c = img.shape # getting the height width and c of camera
                cx,cy = int(lm.x*w) , int(lm.y*h)#using those rations to get to the exac locations of the hand points
                lms.append([id ,cx,cy])
                # print(id , cx,cy)
                if draw:
                    cv2.circle(img , (cx,cy),3, (255,0,0),cv2.FILLED )
            return lms

def main():
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


        cv2.putText(img, "FPS =>"+str(int(fps)), (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 255), 5)
        cv2.imshow("Image ", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main() # main will give overview of what this function can actualy do