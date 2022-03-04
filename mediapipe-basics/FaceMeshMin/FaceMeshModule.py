import cv2
import mediapipe as mp
import  time



class  FaceMeshDetector():
    def __init__(self, mode =False , maxFace =2 , minDetectCon = 0.5 , minTrackConf =0.5):
        self.mpDraw  = mp.solutions.drawing_utils
        self.mpFaceMesh = mp.solutions.face_mesh
        self.faceMesh = self.mpFaceMesh.FaceMesh(static_image_mode=mode, max_num_faces=maxFace , min_detection_confidence=minDetectCon , min_tracking_confidence=minTrackConf)
        self.drawSpec = self.mpDraw.DrawingSpec(color=(234,234,34), thickness=1, circle_radius=1)

    def findFaceMesh(self, img,draw=True):
        Face = []
        Faces = []
        self.imgRgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.faceMesh.process(self.imgRgb)
        if results.multi_face_landmarks:
            for faceLms in results.multi_face_landmarks: # facelms for only one face
                if draw:
                    self.mpDraw.draw_landmarks(img, faceLms, landmark_drawing_spec=self.drawSpec)
                for id,lm in enumerate(faceLms.landmark):
                    ih ,iw, ic = img.shape
                    x,y = int(lm.x*iw), int(lm.y*ih)
                    Face.append([id , x,y])
                Faces.append(Face)
                # print(len(Face))
                # Face = []
                # print("as",len(Face))
                print(Face)

        return img, Faces
def main():
        VIDEO_LINK = [
            "https://vod-progressive.akamaized.net/exp=1646386808~acl=%2Fvimeo-prod-skyfire-std-us%2F01%2F4267%2F21%2F546338711%2F2590712500.mp4~hmac=39e8b7fb3369d3135c62454e81dfbd10a1f3ed33e114d1f2f42b027913bc4858/vimeo-prod-skyfire-std-us/01/4267/21/546338711/2590712500.mp4?filename=pexels-pavel-danilyuk-7812679.mp4",
            "https://vod-progressive.akamaized.net/exp=1646386816~acl=%2Fvimeo-prod-skyfire-std-us%2F01%2F4267%2F21%2F546336084%2F2590700324.mp4~hmac=3669dc011e9387a57ecc7538c3ffc701d0729cb668e8d6549568570b57e6e3d6/vimeo-prod-skyfire-std-us/01/4267/21/546336084/2590700324.mp4?filename=pexels-pavel-danilyuk-7812624.mp4",
            "https://vod-progressive.akamaized.net/exp=1646386789~acl=%2Fvimeo-prod-skyfire-std-us%2F01%2F183%2F16%2F400918020%2F1711529861.mp4~hmac=d0787c0cf23174508c844231141ed13aba702effce745634ddf2fdc5ead5c4f1/vimeo-prod-skyfire-std-us/01/183/16/400918020/1711529861.mp4?filename=production+ID%3A4008398.mp4",
            "https://vod-progressive.akamaized.net/exp=1646386708~acl=%2Fvimeo-prod-skyfire-std-us%2F01%2F3900%2F21%2F544504321%2F2582059071.mp4~hmac=0bd1eaeb42c4eee6a76630190f43b8d506761c6d0a6e15c75ae24701bc497507/vimeo-prod-skyfire-std-us/01/3900/21/544504321/2582059071.mp4?filename=pexels-cottonbro-7760055.mp4"]
        capture = cv2.VideoCapture(VIDEO_LINK[0])
        ptime = 0
        detector =FaceMeshDetector()

        while True:
            sucess, img = capture.read()
            img, Faces = detector.findFaceMesh(img)
            if len(Faces) != 0:
                print(len(Faces))

            ctime = time.time()
            if (ctime - ptime) != 0:
                fps = 1 / (ctime - ptime)
                ptime = ctime
                cv2.putText(img, "FPS =>" + str(int(fps)), (10, 30), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255))

            cv2.imshow("sdf", img)
            cv2.waitKey(1)


if __name__ == "__main__":
    main()
