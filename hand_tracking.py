import cv2
import mediapipe as mp
import time
import handTrackingModule as htm
import math
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


# # def volumeManipulator():
# devices = AudioUtilities.GetSpeakers()
# interface = devices.Activate(
#     IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
# volume = cast(interface, POINTER(IAudioEndpointVolume))
# # volume.GetMute()
# # volume.GetMasterVolumeLevel()
# volumeRange = volume.GetVolumeRange()
# minVolume = volumeRange[0]
# maxVolume = volumeRange[1]



pTime = 0
cTime = 0
cap = cv2.VideoCapture(0)
detector = htm.handDetector(detectionConfid=.7, displayFingerTips=False)
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    thumbUp=True
    indexUp=True
    middleUp=True
    ringUp=True
    pinkyUp=True
    #volumeManipulator()
    if len(lmList) != 0:
        thumbKnucklex,thumbKnuckleY=lmList[2][1], lmList[2][2]
        indexKnuckleX,indexKnuckleY = lmList[6][1],lmList[6][2]
        middleKnuckleX,middleKnuckleY=lmList[10][1],lmList[10][2]
        ringKnuckleX,ringKnuckleY=lmList[14][1],lmList[14][2]
        pinkyKnuckleX,pinkyKnuckleY=lmList[18][1],lmList[18][2]
        
        x1, y1 = lmList[4][1], lmList[4][2]  # get location of thumb

        x2, y2 = lmList[8][1], lmList[8][2]  # get location of index finger

        x3,y3=lmList[12][1],lmList[12][2] #get middle finger location

        x4,y4=lmList[16][1],lmList[16][2] #get ring finger location

        x5,y5=lmList[20][1],lmList[20][2] #get pinky location

        if thumbKnucklex > x1:
            thumbUp=False

        if indexKnuckleY < y2:
            indexUp=False

        if middleKnuckleY <y3:
            middleUp=False

        if ringKnuckleY < y4:
            ringUp=False

        if pinkyKnuckleY <y5:
            pinkyUp=False

        if thumbUp and indexUp and middleUp and ringUp and pinkyUp: #find 5 fingers
            cv2.putText(img,str(5),(lmList[0][1],lmList[0][2]),cv2.FONT_ITALIC,3,(0,0,0),5)

        if indexUp and middleUp and ringUp and pinkyUp and not thumbUp: # 4 fingers
            cv2.putText(img,str(4),(lmList[0][1],lmList[0][2]),cv2.FONT_ITALIC,3,(0,0,0),5)

        if indexUp and middleUp and not ringUp and thumbUp and not pinkyUp: # 3 fingers
            cv2.putText(img,str(3),(lmList[0][1],lmList[0][2]),cv2.FONT_ITALIC,3,(0,0,0),5)

        if indexUp and middleUp and not ringUp  and not thumbUp and not pinkyUp : #2
            cv2.putText(img,str(2),(lmList[0][1],lmList[0][2]),cv2.FONT_ITALIC,3,(0,0,0),5)

        if indexUp and not middleUp and not ringUp  and not thumbUp and not pinkyUp :#1
            cv2.putText(img,str(1),(lmList[0][1],lmList[0][2]),cv2.FONT_ITALIC,3,(0,0,0),5)

        if indexUp and middleUp and ringUp  and  thumbUp and not pinkyUp : #6
            cv2.putText(img,str(6),(lmList[0][1],lmList[0][2]),cv2.FONT_ITALIC,3,(0,0,0),5)

        if indexUp and middleUp and not ringUp  and  thumbUp and pinkyUp :#7
            cv2.putText(img,str(7),(lmList[0][1],lmList[0][2]),cv2.FONT_ITALIC,3,(0,0,0),5)
        
        if indexUp and not middleUp and ringUp  and  thumbUp and  pinkyUp :#8
            cv2.putText(img,str(8),(lmList[0][1],lmList[0][2]),cv2.FONT_ITALIC,3,(0,0,0),5)

        if not indexUp and middleUp and ringUp  and  thumbUp and pinkyUp :#9
            cv2.putText(img,str(9),(lmList[0][1],lmList[0][2]),cv2.FONT_ITALIC,3,(0,0,0),5)
        
        if not indexUp and not middleUp and not ringUp  and  thumbUp and not pinkyUp :#A
            cv2.putText(img,str("A"),(lmList[0][1],lmList[0][2]),cv2.FONT_ITALIC,3,(0,0,0),5)

        if indexUp and middleUp and  ringUp  and not  thumbUp and pinkyUp :#B
            cv2.putText(img,str("B"),(lmList[0][1],lmList[0][2]),cv2.FONT_ITALIC,3,(0,0,0),5)

        print(thumbUp,indexUp,middleUp,ringUp,pinkyUp)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70),
                cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
