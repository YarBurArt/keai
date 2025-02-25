# Keai /

![KeAI by Ayanami Rai](https://raw.githubusercontent.com/YarBurArt/keai/681e1549784fbe8ed8ad0c7e3b2802f9a554b1c5/graphics/be1804782c35e5e74bf24c2884a2b472.jpeg)

This project is practically a friend of mine, with a similar character in speech. The conditional _Ayanami Ray_ can see me, make out my face and hand gestures, and recognise my voice. And then she can respond to me with her voice and show her emotions in a gif.

## Instalation /
```
git clone https://github.com/YarBurArt/keai.git
cd keai
virtualenv venv
```

for linux: `source venv/bin/activate`

for windows: `venv/Scripts/activate`

then install torch via pip3 on https://pytorch.org/get-started/locally/

nightly because python 3.13, and then 

`pip install -r requirements.txt`

Be careful, some packages weigh a lot of gigabytes.

## Run it /

The project is still under active development, not everything has been realised yet, let alone optimised. Here is a guide on how it should work.

(venv) `python3 manager.py` 

OR

Use the individual functions from these files: `handrec.py` , `emorec.py` , `spr2.py` , `imgshow.py` , `autopc.py`
You can also use separately for example `utils/poseimg2txt.py` to generate text of description of emotions and pose from webcam.

## How it works / 

Files: `handrec.py` , `emorec.py` and `spr2.py` receives data from the camera and microphone and transmits it to the manager. 
The manager, based on the ai, triggers a response in the files: `imgshow.py` and `autopc.py`

The project just collects the uses of developments like pytorch, tensorflow, ollama, huggingface and so on into one Ray, a some of its own works and their integration via IPC and python tools. Architecture and model selection on not very powerful hardware. Minimally even integrated graphics. You can use the code in other projects as licensed

## Description /
*Text written by ChatGPT 3.5 and edit by YarBurArt*

The code snippets presented here are intended for eventual integration into a larger program. 
The project would involve developing sophisticated neural networks that can create a highly immersive virtual reality environment, where humans can experience an artificial world that feels just like the real one. The neural networks would be designed to replicate the complex workings of the human speech and its ability to process sensory information, create memories, and generate thoughts and emotions.
In addition to providing an escape from the physical world, the project would also aim to achieve "conditional immortality" through the use of multiple neural networks. These networks would be designed to store and replicate human memories and thought patterns, creating a digital version of the person's mind that could exist indefinitely in the virtual world. You can, for example, communicate with dead people. Neural networks can create a new kind of person...
