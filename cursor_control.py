import pyautogui
import numpy as np
import time
from config import *

plocX, plocY = 0, 0
last_left_click = 0
last_right_click = 0


def move_cursor(index_tip, frame_width, frame_height):
    global plocX, plocY

    x_raw = index_tip.x * frame_width
    y_raw = index_tip.y * frame_height

    targetX = np.interp(x_raw,
                        [FRAME_REDUCTION, frame_width - FRAME_REDUCTION],
                        [0, SCREEN_WIDTH])

    targetY = np.interp(y_raw,
                        [FRAME_REDUCTION, frame_height - FRAME_REDUCTION],
                        [0, SCREEN_HEIGHT])

    targetX = np.clip(targetX, 0, SCREEN_WIDTH - 1)
    targetY = np.clip(targetY, 0, SCREEN_HEIGHT - 1)

    currX = plocX + (targetX - plocX) * SMOOTHING_FACTOR
    currY = plocY + (targetY - plocY) * SMOOTHING_FACTOR

    pyautogui.moveTo(int(currX), int(currY))

    plocX, plocY = currX, currY


def left_click():
    global last_left_click
    if time.time() - last_left_click > CLICK_COOLDOWN:
        pyautogui.click(button='left')
        last_left_click = time.time()


def right_click():
    global last_right_click
    if time.time() - last_right_click > CLICK_COOLDOWN:
        pyautogui.click(button='right')
        last_right_click = time.time()


def scroll_up():
    pyautogui.scroll(SCROLL_SENSITIVITY)


def scroll_down():
    pyautogui.scroll(-SCROLL_SENSITIVITY)