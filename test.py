import cv2
import mediapipe as mp

cap = cv2.VideoCapture(1)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
while True:
    success, image = cap.read()
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(imageRGB)
    # checking whether a hand is detected
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:  # working with each hand
            for id, lm in enumerate(handLms.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                if id == 20:
                    cv2.circle(image, (cx, cy), 25, (255, 0, 255), cv2.FILLED)

                mpDraw.draw_landmarks(image, handLms, mpHands.HAND_CONNECTIONS)
    cv2.imshow("Output", image)
    cv2.waitKey(1)

####################################################################
# import cv2
# import numpy as np
# import HandTracking as ht
# from cvzone.HandTrackingModule import HandDetector
#
# import time
# import autopy
#
# wCam, hCam= 640, 480
# cap = cv2.VideoCapture(1)# number of camera
# cap.set(3,wCam)
# cap.set(4, hCam)
# pTime =0
# smoothening=8
# detector = ht.handDetector(maxHands=1)
# screen_width,screen_height=autopy.screen.size()
# while True:
#     sucess, img = cap.read()
#     img = detector.findHands(img)
#     lmlist,bbox= detector.findPosition(img)#position
#     cTime = time.time()
#     fps = 1 / (cTime - pTime)
#     pTime = cTime
#     cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
#                 (255, 0, 0), 3)
#     cv2.imshow("Image",img)
#     cv2.waitKey(1)
