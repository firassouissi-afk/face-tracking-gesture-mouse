import cv2
import mediapipe as mp
import pyautogui

camera = cv2.VideoCapture(0)
hands = mp.solutions.hands.Hands(max_num_hands=1)
screen_w, screen_h = pyautogui.size()

while camera.isOpened():
    ok, frame = camera.read()
    if not ok:
        break
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)
    if result.multi_hand_landmarks:
        lm = result.multi_hand_landmarks[0].landmark
        index = lm[8]; thumb = lm[4]; middle = lm[12]
        x, y = int(index.x * screen_w), int(index.y * screen_h)
        pyautogui.moveTo(x, y, duration=.05)
        pinch = ((thumb.x-index.x)**2 + (thumb.y-index.y)**2)**.5
        if pinch < .035:
            pyautogui.click()
        cv2.circle(frame, (int(index.x*frame.shape[1]), int(index.y*frame.shape[0])), 8, (0,255,0), -1)
    cv2.imshow("Gesture Mouse - press Q", frame)
    if cv2.waitKey(1) & 0xff == ord("q"):
        break
camera.release()
cv2.destroyAllWindows()
