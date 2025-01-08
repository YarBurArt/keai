import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0) #Камера
hands = mp.solutions.hands.Hands(max_num_hands=0) #Объект ИИ для определения ладони
draw = mp.solutions.drawing_utils #Для рисование ладони
print("debug 0")
while True:
    #Закрытие окна
    if cv2.waitKey(1) & 0xFF == 27:
        break
    print("debug 1")
    success, image = cap.read() #Считываем изображение с камеры
    print("debug 2")
    image = cv2.flip(image, -1) #Отражаем изображение для корекктной картинки
    print("debug 3")
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) #Конвертируем в rgb
    print("debug 4")
    results = hands.process(imageRGB) #Работа mediapipe
    print("debug 5")
    print(results)

    if results.multi_hand_landmarks:
        print("debug 6")
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
            print(handLms)
            draw.draw_landmarks(image, handLms, mp.solutions.hands.HAND_CONNECTIONS) #Рисуем ладонь

    cv2.imshow("Hand", image) #Отображаем картинку