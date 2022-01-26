import time
from Cam_dev import *
from pydexarm import Dexarm
from pick_up import *
import time
import csv
import pickle
from matplotlib import pyplot as plt 
from pick_up import *
from panel_tests import *


'''windows'''
#dexarm = Dexarm(port="COM67")
'''mac & linux'''
dexarm = Dexarm(port= "/dev/serial/by-id/usb-STMicroelectronics_STM32F407ZG_CDC_in_FS_Mode_336336523439-if00")
dexarm_2 = Dexarm(port= "/dev/serial/by-id/usb-STMicroelectronics_STM32F407ZG_CDC_in_FS_Mode_355E358A3236-if00") # initializes dexarm to correct port
loaded_model = pickle.load(open('knnpickle_file_3', 'rb'))

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

def is_pink(av_pixel):
    rm, rs = 190.1140793035982, 64.62080070511523
    gm, gs = 121.38619329631166, 54.87398367095535
    bm, bs = 157.78315867205592, 47.83189991536432
    new_pixel = np.array([(av_pixel[0] - rm)/rs, (av_pixel[1] - gm)/gs, (av_pixel[2] - bm)/bs])
    result = loaded_model.predict(new_pixel.reshape(1, -1)) 
    return result == 'Pink'

# video.close()
# dexarm.go_home()
dexarm.fast_move_to(0, 280, 150)
dexarm.conveyor_belt_stop()
dexarm.conveyor_belt_forward(8300)
video.open(0,320,240)
img = video.get_img(1)[:,:,::-1]
img = trim_image(img)
av_pixel = get_av_pixel(img)
while is_pink(av_pixel):
    img = video.get_img(1)[:,:,::-1]
    img = trim_image(img)
    av_pixel = get_av_pixel(img)
    dexarm.conveyor_belt_forward(8300)

dexarm.conveyor_belt_stop()
plt.imshow(img)
plt.show()
video.close()


# horiz_412(dexarm)

# dexarm.go_home()
# dexarm.fast_move_to(0, 280, 150)
# pile_loc = (-245, 0, -110)
# current = [0, 280, 150]
# move_sample(current[:3], pile_loc, dexarm)