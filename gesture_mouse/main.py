import cv2
import mediapipe as mp
import pyautogui
import time
import numpy as np

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
cap = cv2.VideoCapture(0)
screen_w, screen_h = pyautogui.size()
click_time = 0
windows_minimized = False  # Track if windows are minimized


def get_finger_positions(landmarks, frame_w, frame_h):
    positions = {}
    for id, lm in enumerate(landmarks.landmark):
        x, y = int(lm.x * frame_w), int(lm.y * frame_h)
        positions[id] = (x, y)
    return positions


while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    frame_h, frame_w, _ = frame.shape

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            positions = get_finger_positions(hand_landmarks, frame_w, frame_h)

            index_finger = positions[8]
            middle_finger = positions[12]
            thumb = positions[4]
            ring_finger = positions[16]
            pinky = positions[20]

            # Cursor Movement (Index & Middle Finger Side by Side)
            cursor_x = np.interp(index_finger[0], [0, frame_w], [0, screen_w])
            cursor_y = np.interp(index_finger[1], [0, frame_h], [0, screen_h])
            pyautogui.moveTo(cursor_x, cursor_y)

            # Pinch Gesture for Left Click
            index_thumb_dist = np.linalg.norm(np.array(index_finger) - np.array(thumb))
            if index_thumb_dist < 30:
                if time.time() - click_time > 0.3:
                    pyautogui.click()
                    click_time = time.time()

            # Pinch Middle Finger & Thumb for Right Click
            middle_thumb_dist = np.linalg.norm(np.array(middle_finger) - np.array(thumb))
            if middle_thumb_dist < 30:
                if time.time() - click_time > 0.3:
                    pyautogui.rightClick()
                    click_time = time.time()

            # Ring Finger & Thumb for Right Click Menu
            ring_thumb_dist = np.linalg.norm(np.array(ring_finger) - np.array(thumb))
            if ring_thumb_dist < 30:
                if time.time() - click_time > 0.3:
                    pyautogui.hotkey('shift', 'f10')  # Right-click menu shortcut
                    click_time = time.time()

            # Scroll Gesture (Pinch Index & Middle Finger with Thumb & Move Up/Down)
            if index_thumb_dist < 30 and middle_thumb_dist < 30:
                scroll_speed = int((frame_h // 2) - index_finger[1]) // 5
                pyautogui.scroll(scroll_speed)

            # Drag & Drop (Hold Pinch for 1 sec, Then Move)
            if index_thumb_dist < 30 and time.time() - click_time > 1:
                pyautogui.mouseDown()
                pyautogui.moveTo(cursor_x, cursor_y)
                pyautogui.mouseUp()
                click_time = time.time()

            # Clench Hand to Minimize All Windows, Unclench to Restore
            clenched_hand = all(
                np.linalg.norm(np.array(positions[finger]) - np.array(thumb)) < 30 for finger in [8, 12, 16, 20])
            if clenched_hand and not windows_minimized:
                pyautogui.hotkey('win', 'd')  # Minimize all windows
                windows_minimized = True
                time.sleep(0.5)  # Prevent multiple triggers
            elif not clenched_hand and windows_minimized:
                pyautogui.hotkey('win', 'shift', 'm')  # Restore all minimized windows
                windows_minimized = False

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Gesture Mouse", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
