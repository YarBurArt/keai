""" module to process pose description from web camera  """
from pathlib import Path
import base64
import requests

def encode_image_to_base64(image_path):
    """ standard convert an image file to base64 string"""
    if isinstance(image_path, str) and image_path.startswith("http"):
        response = requests.get(image_path)
        return base64.b64encode(response.content).decode('utf-8')
    else:
        return base64.b64encode(Path(image_path).read_bytes()).decode('utf-8')

def describe_image(base64_image):
    """send image to local Llama API in base
    get text description of the person's pose and emotions"""
    payload = {
        "model": "llama3.2-vision", # update model with you requirements
        "stream": False,
        "messages": [
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
        } ]
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
    #print(f"<Created {image_path.with_suffix('.txt')}>")

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

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        process_directory_or_url(sys.argv[1])
    else:
        process_directory_or_url('.')
