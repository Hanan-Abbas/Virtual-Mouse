import cv2
import numpy as np
import time
from hand_tracker import create_landmarker, detect_hand
from gesture_logic import get_gesture_state
from cursor_control import *
from config import *

# Initialize Camera
cap = cv2.VideoCapture(0)

# Set internal capture resolution (Standard for speed)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Define hand connection pairs for the "Skeleton" look
HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),      # Thumb
    (0, 5), (5, 6), (6, 7), (7, 8),      # Index
    (0, 9), (9, 10), (10, 11), (11, 12), # Middle
    (0, 13), (13, 14), (14, 15), (15, 16), # Ring
    (0, 17), (17, 18), (18, 19), (19, 20), # Pinky
    (5, 9), (9, 13), (13, 17), (0, 17)    # Palm
]

# Set the target size for the window display
DISPLAY_W, DISPLAY_H = 1280, 720

with create_landmarker() as landmarker:
    # Use WINDOW_NORMAL to allow the window to fill the screen space
    cv2.namedWindow("Virtual Control (Privacy Mode)", cv2.WINDOW_NORMAL)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape

        # 1. CREATE THE BLACK SCREEN (Privacy Mode)
        display_screen = np.zeros((h, w, 3), dtype=np.uint8)

        # Detect hands using the actual camera frame
        results = detect_hand(landmarker, frame)

        if results.hand_landmarks:
            for hand_landmarks in results.hand_landmarks:
                
                # 2. DRAW SKELETON ON BLACK SCREEN
                for connection in HAND_CONNECTIONS:
                    start_idx, end_idx = connection
                    pt1 = (int(hand_landmarks[start_idx].x * w), int(hand_landmarks[start_idx].y * h))
                    pt2 = (int(hand_landmarks[end_idx].x * w), int(hand_landmarks[end_idx].y * h))
                    cv2.line(display_screen, pt1, pt2, (255, 255, 255), 2) # White skeleton lines

                for lm in hand_landmarks:
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    cv2.circle(display_screen, (cx, cy), 5, (0, 255, 0), cv2.FILLED) # Green joints

                # 3. GESTURE AND MOUSE LOGIC
                gesture = get_gesture_state(hand_landmarks, CLICK_THRESHOLD)

                if gesture["dist_mid_thumb"] < CLICK_THRESHOLD and gesture["index_up"]:
                    left_click()
                    cv2.putText(display_screen, "LEFT CLICK", (50, 50), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                elif gesture["dist_pinky_thumb"] < CLICK_THRESHOLD and gesture["index_up"]:
                    right_click()
                    cv2.putText(display_screen, "RIGHT CLICK", (50, 50), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                elif gesture["index_up"] and gesture["middle_up"] and not gesture["ring_up"]:
                    scroll_up()
                    cv2.putText(display_screen, "SCROLLING UP", (50, 100), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

                elif not gesture["index_up"] and gesture["middle_up"] and gesture["pinky_up"]:
                    scroll_down()
                    cv2.putText(display_screen, "SCROLLING DOWN", (50, 100), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

                elif gesture["index_up"] and not gesture["middle_up"] and not gesture["pinky_up"]:
                    move_cursor(hand_landmarks[8], w, h)
                    ix, iy = int(hand_landmarks[8].x * w), int(hand_landmarks[8].y * h)
                    cv2.circle(display_screen, (ix, iy), 12, (255, 255, 0), 2)

        # 4. RESIZE THE FINAL IMAGE TO FILL THE WINDOW
       
        resized_view = cv2.resize(display_screen, (DISPLAY_W, DISPLAY_H), interpolation=cv2.INTER_LINEAR)
        
        cv2.imshow("Virtual MouseControl", resized_view)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()