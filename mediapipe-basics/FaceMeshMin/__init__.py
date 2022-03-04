import cv2
import mediapipe as mp
import  time

VIDEO_LINK = ["https://vod-progressive.akamaized.net/exp=1646386808~acl=%2Fvimeo-prod-skyfire-std-us%2F01%2F4267%2F21%2F546338711%2F2590712500.mp4~hmac=39e8b7fb3369d3135c62454e81dfbd10a1f3ed33e114d1f2f42b027913bc4858/vimeo-prod-skyfire-std-us/01/4267/21/546338711/2590712500.mp4?filename=pexels-pavel-danilyuk-7812679.mp4",
              "https://vod-progressive.akamaized.net/exp=1646386816~acl=%2Fvimeo-prod-skyfire-std-us%2F01%2F4267%2F21%2F546336084%2F2590700324.mp4~hmac=3669dc011e9387a57ecc7538c3ffc701d0729cb668e8d6549568570b57e6e3d6/vimeo-prod-skyfire-std-us/01/4267/21/546336084/2590700324.mp4?filename=pexels-pavel-danilyuk-7812624.mp4",
              "https://vod-progressive.akamaized.net/exp=1646386789~acl=%2Fvimeo-prod-skyfire-std-us%2F01%2F183%2F16%2F400918020%2F1711529861.mp4~hmac=d0787c0cf23174508c844231141ed13aba702effce745634ddf2fdc5ead5c4f1/vimeo-prod-skyfire-std-us/01/183/16/400918020/1711529861.mp4?filename=production+ID%3A4008398.mp4",
              "https://vod-progressive.akamaized.net/exp=1646386708~acl=%2Fvimeo-prod-skyfire-std-us%2F01%2F3900%2F21%2F544504321%2F2582059071.mp4~hmac=0bd1eaeb42c4eee6a76630190f43b8d506761c6d0a6e15c75ae24701bc497507/vimeo-prod-skyfire-std-us/01/3900/21/544504321/2582059071.mp4?filename=pexels-cottonbro-7760055.mp4"]
capture = cv2.VideoCapture(VIDEO_LINK[2])
ptime = 0

mpDraw  = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh()
drawSpec = mpDraw.DrawingSpec(color=(234,234,34), thickness=1, circle_radius=1)
while True:
    sucess , img = capture.read()
    imgRgb = cv2.cvtColor(img , cv2.COLOR_BGR2RGB)
    results = faceMesh.process(imgRgb)
    if results.multi_face_landmarks:
        for faceLms in results.multi_face_landmarks: # facelms for only one face
            mpDraw.draw_landmarks(img , faceLms, landmark_drawing_spec=drawSpec)
            #there are total 406 points
            #let's see them one by one
            # print(faceLms.landmark)
            for id,lm in enumerate(faceLms.landmark):
                ih ,iw, ic = img.shape
                x,y = int(lm.x*iw), int(lm.y*ih)
                print(id , x,y)
    ctime = time.time()
    if (ctime - ptime) != 0:
        fps = 1 / (ctime - ptime)
        ptime = ctime
        cv2.putText(img, "FPS =>" + str(int(fps)), (10, 30), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255))

    cv2.imshow("sdf", img)
    cv2.waitKey(1)