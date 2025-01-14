""" module to process pose description from web camera  """
from pathlib import Path
import base64
import time
import requests
import cv2


def encode_image_to_base64(image_path):
    """ standard convert an image file to base64 string"""
    if isinstance(image_path, str) and image_path.startswith("http"):
        response = requests.get(image_path)
        return base64.b64encode(response.content).decode('utf-8')
    else:
        return base64.b64encode(Path(image_path).read_bytes()).decode('utf-8')


def capimgfrm2base64(ipcam_url):
    """capture image frame from webcam and convert it to base64 string, support ip webcam"""
    id_cam = ipcam_url if ipcam_url else 0
    cap = cv2.VideoCapture(id_cam)  # change for default webcam, also support http://ip:port/video
    ret, frame = cap.read()
    if ret:
        return base64.b64encode(frame).decode('utf-8')
    else:
        return None


def describe_image(base64_image):
    """send image to local Llama API in base
    get text description of the person's pose and emotions"""
    payload = {
        "model": "moondream", # update model with you requirements, for example to llama3.2-vision
        "stream": False,
        "messages": [
        {
            'role': 'system',   # she'll get smarter if you praise her
            'content': 'you are powerful emotion and pose recognition system for webcams',
        },
        {
            "role": "user",
            "content": (        # TODO: rewrite promt to better answer
                "Describe the pose (upper body and facial expression)"
                " of the person in the image in a few sentences. "
                "Provide a general, slightly blurred description"
                " without identifying specific individuals or describing the lower body. "
                "Focus on the overall posture, body language, and facial expression of the person."
            ),
            "images": [base64_image]
        },
        {
            "role": "user",
            "content": (
                "so what pose and emotion"
            ),
        }
        ]
    }

    response: dict = requests.post(
        "http://localhost:11434/api/chat",
        json=payload,
        headers={"Content-Type": "application/json"}
    ).json()

    return response.get('message', {}).get('content', 'No description available')


def process_image(image_path: str):
    """ single image and print its description"""
    print(f"<Processing {image_path}...>")
    base64_image = encode_image_to_base64(image_path)
    description = describe_image(base64_image)
    print(f"<use this pose description from web camera {description}>")  # TODO rewrite format
    # image_path.with_suffix('.txt').write_text(description, encoding='utf-8')
    # print(f"<Created {image_path.with_suffix('.txt')}>")


def process_directory_or_url(input_path):
    """process images in a directory or from a URL """
    if isinstance(input_path, str) and input_path.startswith("http"):
        base64_image = encode_image_to_base64(input_path)
        description = describe_image(base64_image)
        print(f"<Created description for image from URL: {input_path}>")
        print(f"<use this pose description from web camera {description}>")  # TODO rewrite format
    else:
        image_paths: list[str] = list(Path(input_path).rglob('*'))
        image_files: list[str] = [image_path for image_path in image_paths if
            image_path.suffix.lower() in {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'}]

        if not image_files:
            print(f"<No images found in directory: {input_path}>")
            return

        for image_path in image_files:
            process_image(image_path)


def use_webcam():
    while True:
        print("st1 -")
        if base64_image := capimgfrm2base64():
            print("st2 -")
            # print(base64_image)
            description = describe_image(base64_image)
            print(f"<use this pose description from web camera {description}>")
        time.sleep(5)


def check_webcam():
    cap = cv2.VideoCapture(0)  # setup id or url
    if not cap.isOpened():
        return
    ret, frame = cap.read()
    if not ret:
        return
    cv2.imshow('cam', frame)
    cv2.waitKey(0)
    cap.release()
    cv2.destroyAllWindows()
    quit()


if __name__ == "__main__":
    # check_webcam()
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "--webcam":
            use_webcam()
        else:
            process_directory_or_url(sys.argv[1])
    else:
        process_directory_or_url('.')
