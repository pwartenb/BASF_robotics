import cv2
import numpy as np
import math
from matplotlib import pyplot as plt
from Cam_dev import *
from pydexarm import Dexarm
from pick_up import *
import time
import pandas as pd
import csv
import pickle

# dexarm = Dexarm(port="/dev/ttyACM0")

def trim_image(im):
    '''
    takes in image and trims to only view conveyor
    belt that is directly under the camera allows 
    for more accurate sensing of panel
    '''
    list_im = list(im)
    x_start = 148
    x_end = 330
    y_start = 270
    y_end = 370
    new_im = list_im[x_start: x_end+1]
    final_im = []
    for item in new_im:
        final_im.append(item[y_start: y_end+1])
    return np.array(final_im)

def get_av_pixel(im):
    '''
    Given spliced image returns average pixel allows
    for more accurate accounting for color change when 
    panel passes underneath the camera
    '''
    total_num = len(im)*len(im[0])
    total = (0, 0, 0)
    for row in im:
        for item in row:
            total += item
    return total/total_num

def get_pic():
    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        raise Exception("Could not open video device")
    ret, frame = video_capture.read()
    video_capture.release()
    im = trim_image(frame[:,:,::-1])
    return im

im = get_pic()
av_pixel = get_av_pixel(im)
print(av_pixel)
plt.imshow(im)
plt.show()
current = int(input("0 for not pink, 1 for pink"))
rows = []
classify = ""
while current != 2:
    if current == 0:
        classify = "Not Pink"
    else:
        classify = "Pink"
    rows.append({'Pixels': list(av_pixel), 'Classification': classify})
    im = get_pic()
    av_pixel = get_av_pixel(im)
    plt.imshow(im)
    plt.show()
    current = int(input("0 for not pink, 1 for pink"))

filename = 'training_data.csv'
fields = ['Pixels', 'Classification']
with open(filename, 'a') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = fields) 
    writer.writerows(rows)