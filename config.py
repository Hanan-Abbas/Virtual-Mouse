import pyautogui

# Screen size

SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
pyautogui.PAUSE = 0
pyautogui.FAILSAFE = True

# Cursor behaviour

SMOOTHING_FACTOR = 0.3
FRAME_REDUCTION = 120
CLICK_THRESHOLD = 0.04
SCROLL_SENSITIVITY = 2

# Click cooldown

CLICK_COOLDOWN = 0.4