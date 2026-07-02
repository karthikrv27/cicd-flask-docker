import cv2
import mediapipe as mp

# Try serial connection safely
try:
    import serial
    ser = serial.Serial('COM3', 9600)
    serial_connected = True
except:
    print("⚠️ Serial not connected")
    serial_connected = False

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
tips = [4, 8, 12, 16, 20]

prev_state = None   

while True:
    ret, frame = cap.read()
    if not ret:
        break

    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            lmList = []

            for lm in handLms.landmark:
                h, w, _ = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append((cx, cy))

            if len(lmList) != 0:
                fingers = []

                # Thumb
                if lmList[4][0] > lmList[3][0]:
                    fingers.append(1)
                else:
                    fingers.append(0)

                # Other fingers
                for id in range(1, 5):
                    if lmList[tips[id]][1] < lmList[tips[id] - 2][1]:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                total = fingers.count(1)

                if total == 1:
                    state = "ON"
                    cv2.putText(frame, "LED ON", (10, 70),
                                cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
                else:
                    state = "OFF"
                    cv2.putText(frame, "LED OFF", (10, 70),
                                cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

                # 🔥 Send only when state changes
                if serial_connected and state != prev_state:
                    if state == "ON":
                        ser.write(b'1')
                    else:
                        ser.write(b'0')
                    prev_state = state

            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()