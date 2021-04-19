import cv2
import mediapipe as mp


class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionConfid=0.5, trackConfid=0.5, displayFingerTips=True):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionConfid = detectionConfid
        self.trackConfid = trackConfid
        self.mpHands = mp.solutions.hands
        self.displayFingerTips = displayFingerTips
        self.hands = self.mpHands.Hands(
            self.mode, self.maxHands, self.detectionConfid, self.trackConfid)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)\

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(
                        img, handLms, self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self, img, handNo=0, draw=True):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                #print(id, cx, cy)
                lmList.append([id, cx, cy])
                if draw:
                    if id == 4 or id == 8 or id == 12 or id == 16 or id == 20:
                        cv2.circle(img, (cx, cy), 15,
                                   (255, 0, 255), cv2.FILLED)
                        if self.displayFingerTips:
                            cv2.putText(img, str(id), (cx-5, cy-10),
                                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 3)

        return lmList
