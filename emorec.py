import cv2
import matplotlib.pyplot as plt
import bleedfacedetector as fd
import numpy as np
import time
import os

import imgshow


def init_emotion(
    model="models/emotion-ferplus-8.onnx"
    ):
    # Set global variables
    global net, emotions

    # Define the emotions
    emotions = ['Neutral', 'Happy', 'Surprise', 
                'Sad', 'Anger', 'Disgust',
                'Fear', 'Contempt']

    # Initialize the DNN module
    net = cv2.dnn.readNetFromONNX(model)


def emotion(image, returndata=False):
    # Make copy of  image
    img_copy = image.copy()
    # Detect faces in image
    faces = fd.ssd_detect(img_copy, conf=0.2)
    # Define padding for face ROI
    padding = 3

    # Iterate process for all detected faces
    for x, y, w, h in faces:
        # Get the Face from image
        face = img_copy[y - padding:y + h + padding,
                        x - padding:x + w + padding]

        # Convert the detected face from BGR to Gray scale
        gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        # Resize the gray scale image into 64x64
        resized_face = cv2.resize(gray, (64, 64))
        # Reshape the final image in required format of model
        processed_face = resized_face.reshape(1, 1, 64, 64)
        # Input the processed image
        net.setInput(processed_face)
        # Forward pass
        Output = net.forward()
        # Compute softmax values for each sets of scores
        expanded = np.exp(Output - np.max(Output))
        probablities = expanded / expanded.sum()
        # Get the final probablities by getting rid of any extra dimensions
        prob = np.squeeze(probablities)

        # Get the predicted emotion
        predicted_emotion = emotions[prob.argmax()]
        print(predicted_emotion)
        if predicted_emotion == 'Happy':
            imgshow.showimg_tk('graphics/r1.png', "it's good that you feel alive")
        # Write predicted emotion on image
        cv2.putText(img_copy, '{}'.format(predicted_emotion),
                    (x, y + h + (1 * 20)), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (255, 0, 255),
                    2, cv2.LINE_AA)
        # Draw a rectangular box on the detected face
        cv2.rectangle(img_copy, (x, y), 
                     (x + w, y + h), 
                     (0, 0, 255), 2)

    if returndata:
        # Return the the final image if return data is True
        return img_copy

    else:
        # Displpay the image
        plt.figure(figsize=(10, 10))
        plt.imshow(img_copy[:, :, ::-1])
        plt.axis("off")


fps = 0
init_emotion()
cap = cv2.VideoCapture(0)
# src = cv2.cuda_GpuMat()
# If you want to use the webcam the pass 0
# cap = cv2.VideoCapture(0)

while True:
    while True:
        time.sleep(0.2)  # the optimization fps and cpu resource
        start_time = time.time()
        ret, frame = cap.read()
          
        # src = cv2.cuda_GpuMat().upload(frame)
        # clahe = cv2.cuda.createCLAHE(clipLimit=5.0, tileGridSize=(8, 8))
        # frame = clahe.apply(src, cv2.cuda_Stream.Null()).download()


        if not ret:
            break

        image = cv2.flip(frame, 1)
        image = emotion(image, returndata=True)

        cv2.putText(image, 'FPS: {:.2f}'.format(fps), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 20, 55), 1)
        cv2.imshow("Emotion Recognition", image)

        fps = (1.0 / (time.time() - start_time))

        k = cv2.waitKey(1)
        if k == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
