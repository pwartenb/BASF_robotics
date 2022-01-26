import cv2
import numpy as np
import math
from matplotlib import pyplot as plt
from Cam_dev import *
from pydexarm import Dexarm
from pick_up import *
from panel_tests import *
import time
import csv
import pickle

'''windows'''
#dexarm = Dexarm(port="COM67")
'''mac & linux'''
loaded_model = pickle.load(open('knnpickle_file_aug', 'rb'))
dexarm_2 = Dexarm(port= "/dev/serial/by-id/usb-STMicroelectronics_STM32F407ZG_CDC_in_FS_Mode_355E358A3236-if00") # initializes dexarm to correct port
dexarm = Dexarm(port= "/dev/serial/by-id/usb-STMicroelectronics_STM32F407ZG_CDC_in_FS_Mode_336336523439-if00")

draw_35 = [cross_35, vert_35]
draw_46 = [cross_46, vert_46, angle_46, horiz_46]
draw_48 = [cross_48, vert_48, angle_48, horiz_48]
draw_412 = [cross_412, vert_412, angle_412, horiz_412]

def trim_image(im): #415
    '''
    takes in image and trims to only view conveyor
    belt that is directly under the camera allows 
    for more accurate sensing of panel
    '''
    list_im = list(im)
    x_start = 58
    x_end = 148
    y_start = 135
    y_end = 185
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

def align_panel(dexarm, func):
    '''
    Takes in time elapsed from panel passing through camera,
    a dexarm instance, and func that correlates to panel test.
    Function moves panel so samples can be taken accurately
    '''
    func(dexarm) # takes samples
    dexarm.dealy_s(1)
    
def find_length(dexarm, test_type):
    '''
    Takes in Dexarm instance and time that panel began to move.
    Calculates length of panel and chooses corresponding test program
    then returns panel to mosition under vacuum pump so it can be
    placed on the done pile. Returns nothing.
    '''
    current = [True, True, True]
    start = time.perf_counter()
    video.open(0,320,240)
    while current.count(True) > 1: # loops until panel is viewed
        img = video.get_img(1)[:,:,::-1]
        img = trim_image(img)
        av_pixel = get_av_pixel(img)
        current.pop(0)
        current.append(is_pink(av_pixel))

    end = time.perf_counter()
    elapsed = end - start
    dist = elapsed*71.0
    length = (400 - dist)/25.4 # length of panel based on time from drop until it reaches the camera
    if 3 < length < 5.5:
        print("3x5 Panel")
        t = (length - 5)*25.4/71
        if t > 0:
            time.sleep(t)
        if test_type < 2:
            func = draw_35[test_type]
            align_panel(dexarm, func)
        else:
            print("This test does not apply to 3x5 panels")
    elif 5.5 < length < 7: # based on range of possible lengths determines corresponding panel size
        print("4x6 Panel")
        t = (length - 6)*25.4/71
        if t > 0:
            time.sleep(t)
        func = draw_46[test_type] 
        align_panel(dexarm, func) # alignes panel based on size and chooses corresponging function
    elif 7 < length < 9.5:
        print("4x8 Panel")
        t = (length - 8)*25.4/71
        if t > 0:
            time.sleep(t)
        func = draw_48[test_type]
        align_panel(dexarm, func)
    elif 9.5 < length < 15:
        print("4x12 Panel")
        t = ((length - 12)*25.4/71)
        if t > 0:
            time.sleep(t)
        func = draw_412[test_type]
        align_panel(dexarm, func)
    dexarm.conveyor_belt_forward(8300)
    video.close()

def all_same(dexarm, test_type, size):
    '''
    Takes in Dexarm instance, type of test that is to be done, and panel size.
    Adjusts panel and then performs test. This is only called when all 
    panels are the same size. Returns nothing
    '''
    dexarm.conveyor_belt_forward(8300)
    if size == 0:
        time.sleep(3.8) # test time for 3x5
        func = draw_35[test_type]
        align_panel(dexarm, func)
    elif size == 1:
        time.sleep(3.5) # test time for 4x6
        func = draw_46[test_type]
        align_panel(dexarm, func)
    elif size == 2:
        time.sleep(2.8) # test time for 4x8
        func = draw_48[test_type]
        align_panel(dexarm, func)
    elif size == 3:
        time.sleep(1.9) # test time for 4x12
        func = draw_412[test_type]
        align_panel(dexarm, func)    
    dexarm.conveyor_belt_forward(8300)

def run_test(dexarm, dexarm_2 = 0, pile_loc = 0, test_type = 0, size = None):
    '''
    Takes in two dexarm objects. One should have probe attached other
    has vacuum pump. Moves panels to conveyor belt and then
    calls function to find length and engage probe 
    '''
    dexarm.fast_move_to(0, 330 - 50, 150)
    current = [0, 280, 150]
    move_sample(current[:3], pile_loc, dexarm_2) # gets panel off the pile
    if size is not None:
        all_same(dexarm, test_type, size) # all panels are same size
    else:
        find_length(dexarm, test_type)

def is_pink(av_pixel):
    '''
    Takes in average rgb pixel values, normalizes it, and inputs it into model
    Output is boolean value of whether the camera is over tape or panel
    '''
    total = sum(av_pixel)/3
    if total > 251: # filters out when there is excessive camera glare (picture is completely white)
        return True
    rm, rs = 190.1140793035982, 64.62080070511523 # mean and std for each index of rgb tuple
    gm, gs = 121.38619329631166, 54.87398367095535
    bm, bs = 157.78315867205592, 47.83189991536432
    new_pixel = np.array([(av_pixel[0] - rm)/rs, (av_pixel[1] - gm)/gs, (av_pixel[2] - bm)/bs]) # normalizes tuple values
    result = loaded_model.predict(new_pixel.reshape(1, -1)) #prediction of model
    return result == 'Pink'

if __name__ == "__main__":
    dexarm.go_home()
    dexarm_2.go_home()
    print("Ready to go")
    dexarm.fast_move_to(0, 280, 150)
    dexarm_2.fast_move_to(0, 280, 150)
    dexarm.conveyor_belt_forward(8300)
    num_panels = int(input('How many panels?: '))
    remaining = num_panels
    test_type = int(input('Press 1 for cross pattern, 2 for vertical, 3 for angled, and 4 for horizontal: '))
    same_size = int(input('Press 1 if all panels same size, otherwise 2: '))
    if same_size == 1:
        size = int(input('Press 1 for all 3x5, 2 for all 4x6, 3 for all 4x8, 4 for all 4x12: '))
    for i in range(num_panels):
        if remaining > 15: # z location of pil is moved up when a large number of panels is present
            dif = remaining - 20
            inc = int(dif/5)
            pile_loc = (-245, 0, -110 + inc)
        else:
            pile_loc = (-245, 0, -110)
        if same_size == 1: # all panles are same size
            run_test(dexarm, dexarm_2, pile_loc, test_type - 1, size - 1) 
        else:
            run_test(dexarm, dexarm_2, pile_loc, test_type - 1)
        remaining -= 1
    time.sleep(3)
    dexarm.conveyor_belt_stop()
