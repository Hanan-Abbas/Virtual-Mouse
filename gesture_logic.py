import math


def get_gesture_state(hand_landmarks, click_threshold):
    thumb_tip = hand_landmarks[4]
    index_tip, index_mcp = hand_landmarks[8], hand_landmarks[5]
    middle_tip, middle_mcp = hand_landmarks[12], hand_landmarks[9]
    pinky_tip, pinky_mcp = hand_landmarks[20], hand_landmarks[17]
    ring_up = hand_landmarks[16].y < hand_landmarks[13].y

    # Distances
    dist_mid_thumb = math.hypot(middle_tip.x - thumb_tip.x,
                                middle_tip.y - thumb_tip.y)

    dist_pinky_thumb = math.hypot(pinky_tip.x - thumb_tip.x,
                                  pinky_tip.y - thumb_tip.y)

    # Finger states
    index_up = index_tip.y < index_mcp.y
    middle_up = middle_tip.y < middle_mcp.y
    pinky_up = pinky_tip.y < pinky_mcp.y

    return {
        "index_up": index_up,
        "middle_up": middle_up,
        "pinky_up": pinky_up,
        "ring_up": ring_up,
        "dist_mid_thumb": dist_mid_thumb,
        "dist_pinky_thumb": dist_pinky_thumb
    }