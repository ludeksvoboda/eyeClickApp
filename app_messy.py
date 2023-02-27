from PIL import Image
import json

def save_image(array, image_path):
    """saves numpy array as image"""
    img = Image.fromarray(array)
    img.save(image_path)

def save_dict_to_json(dict, json_path):
    """saves dictionary to json"""
    with open(json_path, 'w') as f:
        json.dump(dict, f)

def  read_dict_from_json(json_path):
    """reads dictionary from json"""
    with open(json_path, 'r') as f:
        return json.load(f)

import pygame
import pygame.camera
import requests
import cv2
from pynput.mouse import Controller
import pandas as pd


SAVEDIR = "/home/lu/MLData/EyeClickApp/tests/"
url = "http://10.0.0.21:8080/predictions/effnet"
mouse = Controller()
pygame.init()
pygame.camera.init()
cam = pygame.camera.Camera("/dev/video1", (640, 480))
cam.start()
    
i = 0
eval_data_list = []
while True:
    img = pygame.surfarray.array3d(cam.get_image()).swapaxes(0,1)
    # image_path = SAVEDIR + "test_"+ str(i) +".png"
    # save_image(img, image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.imencode('.png', img)[1].tobytes()
    response_bytes = requests.put(url, data=img)
    data = response_bytes.text
    # print(data)
    data = json.loads(data)
    position_adjusted = (data["data"][0][0]+ 960, -data["data"][0][1] + 540)
    mouse.position = position_adjusted
    # eval_data_list.append([image_path, data["data"][0][0], data["data"][0][1]])
    # print(i)
    # if i == 100:
    #     eval_df = pd.DataFrame(eval_data_list, columns=["path", "x", "y"])
    #     eval_df.to_csv("eval_data.csv")
    #     break
    # i += 1