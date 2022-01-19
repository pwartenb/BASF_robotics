import time
from Cam_dev import *
from pydexarm import Dexarm
from pick_up import *
import time
import csv
import pickle
from matplotlib import pyplot as plt 

'''windows'''
#dexarm = Dexarm(port="COM67")
'''mac & linux'''
dexarm = Dexarm(port="/dev/ttyACM0")
loaded_model = pickle.load(open('knnpickle_file_3', 'rb'))

def trim_image(im):
    '''
    takes in image and trims to only view conveyor
    belt that is directly under the camera allows 
    for more accurate sensing of panel
    '''
    list_im = list(im)
    x_start = 82
    x_end = 172
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
    rm, rs = 188.3378184797758, 65.11833826181713
    gm, gs = 120.33748490909115, 53.352200935211435
    bm, bs = 155.1103771075327, 47.97257529192781
    new_pixel = np.array([(av_pixel[0] - rm)/rs, (av_pixel[1] - gm)/gs, (av_pixel[2] - bm)/bs])
    result = loaded_model.predict(new_pixel.reshape(1, -1)) 
    return result

video.open(0,320,240)
dexarm.go_home()
dexarm.fast_move_to(0, 330, 150)
img = video.get_img(0)[:,:,::-1]
img = trim_image(img)
av_pixel = get_av_pixel(img)
new = is_pink(av_pixel)
print(new)
dexarm.conveyor_belt_forward(8300)
while new != 'Pink':
    img = video.get_img(0)[:,:,::-1]
    img = trim_image(img)
    av_pixel = get_av_pixel(img)
    new = is_pink(av_pixel)
    # print(new)

dexarm.conveyor_belt_stop()
video.close()
plt.imshow(img)
plt.show()