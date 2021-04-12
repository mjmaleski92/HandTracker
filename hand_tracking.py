import cv2
import mediapipe as mp
import time
import handTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


def volumeManipulator():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    # volume.GetMute()
    # volume.GetMasterVolumeLevel()
    volumeRange = volume.GetVolumeRange()
    minVolume = volumeRange[0]
    maxVolume = volumeRange[1]
    #volume.SetMasterVolumeLevel(-20.0, None)


pTime = 0
cTime = 0
cap = cv2.VideoCapture(0)
detector = htm.handDetector(detectionConfid=.7, displayFingerTips=False)
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    volumeManipulator()
    if len(lmList) != 0:
        x1, y1 = lmList[4][1], lmList[4][2]  # get location of thumb

        x2, y2 = lmList[8][1], lmList[8][2]  # get location of index finger
        # find midpoint between the two fingers
        cx, cy = (x1+x2)//2, (y1+y2)//2

        cv2.line(img, (x1, y1), (x2, y2), (255, 255, 0), 3)
        cv2.circle(img, (cx, cy), 10, (255, 30, 50), cv2.FILLED)

        length = math.hypot(x2-x1, y2-y1)
        if length < 30:
            cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)
        print(length)

        # hand range 200 to 30
        # volume range is -65.25 - 0

        vol = np.interp(length, [30, 200], [minVolume, maxVolume])
        print(vol)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70),
                cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
