import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

cap = cv2.VideoCapture(0)

def print_result(result: HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    print('hand landmarker result: {}'.format(result))

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path='models/hand_landmarker.task'),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result)

while True:
    success, img = cap.read()
    with HandLandmarker.create_from_options(options) as landmarker:
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img)
        landmarker.detect_async(mp_image, 2)
    # cv2.imshow(cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR))

    # Wait for user input - q, then you will stop the loop
    key_pressed = cv2.waitKey(1) & 0xFF  # it will wait for 1 mili second bitwise and
    if key_pressed == ord('q'):  # ord tells you ascii value of that character
        break

cap.release()
cv2.destroyALlWindows()
