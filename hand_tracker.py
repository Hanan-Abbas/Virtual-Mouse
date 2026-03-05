import mediapipe as mp
import cv2
import time

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode


def create_landmarker(model_path="models/hand_landmarker.task"):
    options = HandLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=model_path),
        running_mode=VisionRunningMode.VIDEO,
        num_hands=1
    )
    return HandLandmarker.create_from_options(options)


def detect_hand(landmarker, frame):
    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    )
    timestamp = int(time.time() * 1000)
    return landmarker.detect_for_video(mp_image, timestamp)