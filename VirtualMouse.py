# import cv2
# import numpy as np
# import HandTracking as ht
# import time
# import autopy
#
# ##########################
# wCam, hCam = 640, 480
# frameR = 100  # Frame Reduction
# smoothening = 8
# #########################
#
# pTime = 0
# plocX, plocY = 0, 0
# clocX, clocY = 0, 0
#
# cap = cv2.VideoCapture(0)
# cap.set(3, wCam)
# cap.set(4, hCam)
# detector = ht.handDetector(maxHands=1)
# wScr, hScr = autopy.screen.size()
# # print(wScr, hScr)
#
# while True:
#     # 1. Find hand Landmarks
#     success, img = cap.read()
#     img = detector.findHands(img)
#     lmList, bbox = detector.findPosition(img)
#     # 2. Get the tip of the index and middle fingers
#     if len(lmList) != 0:
#         x1, y1 = lmList[8][1:]
#         x2, y2 = lmList[12][1:]
#         #print(x1, y1, x2, y2)
#
#     # 3. Check which fingers are up
#     fingers = detector.fingersUp()
#     # print(fingers)
#     cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
#                   (255, 0, 255), 2)
#     # 4. Only Index Finger : Moving Mode
#     if fingers[1] == 1 and fingers[2] == 0:
#         # 5. Convert Coordinates
#         x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
#         y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
#         # 6. Smoothen Values
#         clocX = plocX + (x3 - plocX) / smoothening
#         clocY = plocY + (y3 - plocY) / smoothening
#
#         # 7. Move Mouse
#         autopy.mouse.move(wScr - clocX, clocY)
#         cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
#         plocX, plocY = clocX, clocY
#
#     # 8. Both Index and middle fingers are up : Clicking Mode
#     if fingers[1] == 1 and fingers[2] == 1:
#         # 9. Find distance between fingers
#         length, img, lineInfo = detector.findDistance(8, 12, img)
#         print(length)
#         # 10. Click mouse if distance short
#         if length < 40:
#             cv2.circle(img, (lineInfo[4], lineInfo[5]),
#                        15, (0, 255, 0), cv2.FILLED)
#             autopy.mouse.click()
#
#     # 11. Frame Rate
#     cTime = time.time()
#     fps = 1 / (cTime - pTime)
#     pTime = cTime
#     cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
#                 (255, 0, 0), 3)
#     # 12. Display
#     cv2.imshow("Image", img)
#     cv2.waitKey(1)
import cv2
import numpy as np
import time
import HandTracking as ht
import autopy

# Install using "pip install autopy"

### Variables Declaration
pTime = 0               # Used to calculate frame rate
width = 640             # Width of Camera
height = 480            # Height of Camera
frameR = 100            # Frame Rate
smoothening = 8         # Smoothening Factor
prev_x, prev_y = 0, 0   # Previous coordinates
curr_x, curr_y = 0, 0   # Current coordinates

cap = cv2.VideoCapture(0)   # Getting video feed from the webcam
cap.set(3, width)           # Adjusting size
cap.set(4, height)

detector = ht.handDetector(maxHands=1)                  # Detecting one hand at max
screen_width, screen_height = autopy.screen.size()      # Getting the screen size
while True:
    success, img = cap.read()
    img = detector.findHands(img)                       # Finding the hand
    lmlist, bbox = detector.findPosition(img)           # Getting position of hand

#cordination of index and middle finger
    if len(lmlist)!=0:
        x1, y1 = lmlist[8][1:]#tip id
        x2, y2 = lmlist[12][1:]

        fingers = detector.fingersUp()      # Checking if fingers are upwards
        cv2.rectangle(img, (frameR, frameR), (width - frameR, height - frameR), (255, 0, 255), 2)   # Creating boundary box
        if fingers[1] == 1 and fingers[2] == 0:     # If index finger is up and middle finger is down
            x3 = np.interp(x1, (frameR,width-frameR), (0,screen_width))
            y3 = np.interp(y1, (frameR, height-frameR), (0, screen_height))

            curr_x = prev_x + (x3 - prev_x)/smoothening
            curr_y = prev_y + (y3 - prev_y) / smoothening

            autopy.mouse.move(screen_width - curr_x, curr_y)    # Moving the cursor
            cv2.circle(img, (x1, y1), 7, (255, 0, 255), cv2.FILLED)
            prev_x, prev_y = curr_x, curr_y

        if fingers[1] == 1 and fingers[2] == 1:     # If fore finger & middle finger both are up
            length, img, lineInfo = detector.findDistance(8, 12, img)

            if length < 40:     # If both fingers are really close to each other
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()    # Perform Click
##############################
    # check whether index finger and middle finger is up

        x4, y4 = lmlist[8][1:]  # tip id
        x5, y5 = lmlist[12][1:]
        if fingers[1] == 1 and fingers[2] == 2:
            length, img, lineInfo = detector.findDistance(8, 12, img)

            if length == 40:  # If both fingers are really close to each other
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                autopy.mouse.LEFT_BUTTON()

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)