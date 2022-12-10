import imgshow

imgshow.show("graphics/r1.png", "hello man, how are you doing")
answer = input(">>")
if "good" in answer.split():
    imgshow.show("graphics/r1.png", "It's good that you're okay")

