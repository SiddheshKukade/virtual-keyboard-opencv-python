import cv2
import mediapipe as mp
import time


class FaceDetector():
    def __init__(self):
        self.mpFaceDetection = mp.solutions.face_detection
        self.mpDraw = mp.solutions.drawing_utils
        self.faceDetection = self.mpFaceDetection.FaceDetection()

    def findFaces(self ,img, draw = True ):
        imgRgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.faceDetection.process(imgRgb)
        bboxs  = []
        if self.results.detections:
            for id ,detection  in enumerate(self.results.detections):
                bboxC = detection.location_data.relative_bounding_box
                ih , iw , ic = img.shape
                bbox = int(bboxC.xmin * iw),  int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
                bboxs.append([id , bbox , detection.score])
                cv2.putText(img, "Confidence =>" + str("{:.0f}".format(detection.score[0] * 100)) + "%", (100, 100),
                            cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255))
                img = self.fancy_draw(img , bbox)
                if draw:

                    cv2.rectangle(img , bbox , (255,0,255), 2 )


        return img ,  bboxs

    def fancy_draw(self, img , bbox, l=30 , t=5):
        x ,y ,w ,h = bbox # we will get the starting point of box as x and y co-ordinates
        # here we are getting the  right side top and bottom points of rectangle
        x1 , y1 = x+w , y+h
        print("in fancy ",img)
        # top right x,y
        cv2.line(img=img ,pt1= (x,y),pt2= (x+l , y),color=(34,35,243),thickness= t)
        cv2.line(img=img ,pt1= (x,y),pt2= (x , y+l),color=(34,35,243),thickness= t)
        # top right x1, y
        cv2.line(img=img, pt1=(x1, y), pt2=(x1 -  l, y), color=(34, 35, 243), thickness=t)
        cv2.line(img=img, pt1=(x1, y), pt2=(x1 , y + l), color=(34, 35, 243), thickness=t)
        # bottom left x,y1
        cv2.line(img=img, pt1=(x, y1), pt2=(x + l, y1), color=(34, 35, 243), thickness=t)
        cv2.line(img=img, pt1=(x, y1), pt2=(x, y1 - l), color=(34, 35, 243), thickness=t)
        # bottom right x1 ,y1
        cv2.line(img=img, pt1=(x1, y1), pt2=(x1 - l, y1), color=(34, 35, 243), thickness=t)
        cv2.line(img=img, pt1=(x1, y1), pt2=(x1, y1 -l), color=(34, 35, 243), thickness=t)

        return img
def main():
    VIDEO_LINK = [
        "https://vod-progressive.akamaized.ntet/exp=1646386808~acl=%2Fvimeo-prod-skyfire-std-us%2F01%2F4267%2F21%2F546338711%2F2590712500.mp4~hmac=39e8b7fb3369d3135c62454e81dfbd10a1f3ed33e114d1f2f42b027913bc4858/vimeo-prod-skyfire-std-us/01/4267/21/546338711/2590712500.mp4?filename=pexels-pavel-danilyuk-7812679.mp4",
        "https://vod-progressive.akamaized.net/exp=1646386816~acl=%2Fvimeo-prod-skyfire-std-us%2F01%2F4267%2F21%2F546336084%2F2590700324.mp4~hmac=3669dc011e9387a57ecc7538c3ffc701d0729cb668e8d6549568570b57e6e3d6/vimeo-prod-skyfire-std-us/01/4267/21/546336084/2590700324.mp4?filename=pexels-pavel-danilyuk-7812624.mp4",
        "https://vod-progressive.akamaized.net/exp=1646386789~acl=%2Fvimeo-prod-skyfire-std-us%2F01%2F183%2F16%2F400918020%2F1711529861.mp4~hmac=d0787c0cf23174508c844231141ed13aba702effce745634ddf2fdc5ead5c4f1/vimeo-prod-skyfire-std-us/01/183/16/400918020/1711529861.mp4?filename=production+ID%3A4008398.mp4",
        "https://vod-progressive.akamaized.net/exp=1646386708~acl=%2Fvimeo-prod-skyfire-std-us%2F01%2F3900%2F21%2F544504321%2F2582059071.mp4~hmac=0bd1eaeb42c4eee6a76630190f43b8d506761c6d0a6e15c75ae24701bc497507/vimeo-prod-skyfire-std-us/01/3900/21/544504321/2582059071.mp4?filename=pexels-cottonbro-7760055.mp4"]
    cap = cv2.VideoCapture(VIDEO_LINK[3])
    ptime = 0
    detector = FaceDetector()
    while True:
        sucess, img = cap.read()
        print("Before", img)

        img,bboxes = detector.findFaces(img,False )
        print("After", img)

        ctime = time.time()
        if (ctime - ptime) != 0:
            fps = 1 / (ctime - ptime)
            ptime = ctime
            cv2.putText(img, "FPS =>" + str(int(fps)), (10, 30), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 0, 255))

        cv2.imshow('face Detection', img)
        cv2.waitKey(10)


if __name__ == "__main__":
    main()