import time

import cv2
import mediapipe as mp

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
# static image model if true whole time will do detection which is slower so we will set it to false
# we can also set maximun number of hands
#  we can keep all default parameters

ptime = 0
ctime = 0

cap = cv2.VideoCapture(1)
while True:

    sucess, img = cap.read()
    # print(img.shape)
    # we need to send RGB image to hands
    imageRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imageRGB)  # every time hands obj will try to find hands and store them in 'results'
    # extracting multiple hands
    # print(results.multi_hand_landmarks) # wil give us co-ordinates whenever it sees some hands
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:  # the co-ordinates can be of multiple hands hence we are using a for loop to get co-ordinated of only singele hand one by one
            # method provided by MP to draw the lines between hand points
            # print(handLms)
            # sample handLMs=
            # landmark {
            #   x: 0.415691614151001
            #   y: 0.48311102390289307
            #   z: -0.038612112402915955
            # }
            # Enumerate() method adds a counter to an iterable and returns it in a form of enumerating object
                for id ,lm in enumerate(handLms.landmark):  # WE ARE JUST ENUMERATING ONLY ENTIRE SINGLE HAND
                    # we get ratio of the image from x and y pointsf
                    h,w,c = img.shape # getting the height width and c of camera
                    cx,cy = int(lm.x*w) , int(lm.y*h)#using those rations to get to the exac locations of the hand points
                    print(id , cx,cy)
                    # sample Out-put each id represents a point on hand
                    # 0 351 349
                    # 1 408 315
                    # 2 447 278
                    # 3 462 236
                    # 4 463 195
                    # 5 412 203
                    # 6 436 151
                    # 7 456 167
                    # 8 463 194
                    # 9 385 199
                    # 10 408 149
                    # 11 423 178
                    # 12 423 214
                    # 13 355 196
                    # 14 377 149
                    # 15 393 174
                    # 16 395 211
                    # 17 321 198
                    # 18 339 159
                    # 19 357 172
                    # 20 363 197
                    if id ==0:# we are printing circle on hand co-ordinate whose id is 0 in this case the center bottom of the palm you can experiment with different ids

                        cv2.circle(img , (cx,cy),25, (255,0,0),cv2.FILLED )
        mpDraw.draw_landmarks(img, handLms,mpHands.HAND_CONNECTIONS)  # we are not using imgRGB becuse we are not displaying that image on screen we are displaying our original BGR image

            # let's see how to see current camera frame rate
    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime
    # print(time.time())

    cv2.putText(img, str(int(fps)), (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 255), 5)
    cv2.imshow("Image ", img)
    cv2.waitKey(1)
