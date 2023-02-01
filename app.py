import numpy as np
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

SAVEDIR = "/home/lu/MLData/EyeClickApp/tests/"
url = "http://10.0.0.21:8080/predictions/resnet-18"
pygame.init()
pygame.camera.init()
cam = pygame.camera.Camera("/dev/video1", (640, 480))
cam.start()

import _thread

def input_thread(a_list):
    input()             # use input() in Python3
    a_list.append(True)
    
def do_stuff():
    a_list = []
    _thread.start_new_thread(input_thread, (a_list,))
    i = 0
    while True:
        img = pygame.surfarray.array3d(cam.get_image()).swapaxes(0,1)
        image_path = SAVEDIR + "test_"+ str(i) +".png"
        save_image(img, image_path)
        response = requests.put(url, data=open(image_path,'rb').read())
        results[image_path] = response.text
        i += 1

        if a_list:
            save_dict_to_json(results, "results.json")
            break

i  = 0
results = {}
while True:
    img = pygame.surfarray.array3d(cam.get_image()).swapaxes(0,1)
    image_path = SAVEDIR + "test_"+ str(i) +".png"
    save_image(img, image_path)
    response = requests.put(url, data=open(image_path,'rb').read())
    results[image_path] = response.text

    i += 1