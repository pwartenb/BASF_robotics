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

tar_color = 'green'
color_dict = {'red': {'Lower': np.array([127, 60, 171]), 'Upper': np.array([188, 197, 255])},
              'blue': {'Lower': np.array([100, 80, 46]), 'Upper': np.array([124, 255, 255])},
              'green': {'Lower': np.array([35, 43, 35]), 'Upper': np.array([90, 255, 255])},
              }              

red_hsv = [108, 190, 120, 255, 163, 223]
blue_hsv = [74, 131, 107, 241, 146, 255]
yellow_hsv = [30, 83, 60, 209, 156, 255]

feature_param=[40,40,60,250,20]

rgb_param=[0,0,255]

draw_35 = [cross_35, vert_35]
draw_46 = [cross_46, vert_46, angle_46, horiz_46]
draw_48 = [cross_48, vert_48, angle_48, horiz_48]
draw_412 = [cross_412, vert_412, angle_412, horiz_412]

class Color_block_recogn():
    tar_num = 0

    tar_info = {"num":0,
            "center":[],
            "angle":[]}
    

    def __init__(self,color_list=[],fea_list=[],rect_rgb_list=[]):
        self.hsv = color_list
        self.fea_p = fea_list
        self.rect_rgb = rect_rgb_list
        print("Color hsv"+str(self.hsv))
        print("Target characteristics"+str(self.fea_p))
        print("Rectangular border"+str(self.rect_rgb))
        pass
    
    def set_hsv(self,tar_list=[]):
        self.hsv = tar_list
        pass

    def set_fea(self,tar_list=[]):
        self.fea_p = tar_list
        pass

    def set_rect_rgb(self,tar_list=[]):
        self.rect_rgb = tar_list
        pass

    def get_target_img(self,img,condition_index):
        

        temp_tar_info = {"num":0,
        "center":[],
        "angle":[]}
        temp_num = 0


        gs_img = cv2.GaussianBlur(img, (5, 5), 0)                     

        hsv_img = cv2.cvtColor(gs_img, cv2.COLOR_BGR2HSV)

        inRange_hsv = cv2.inRange(hsv_img, np.array([self.hsv[0],self.hsv[2],self.hsv[4]]), np.array([self.hsv[1],self.hsv[3],self.hsv[5]]))

        average_val_img = cv2.blur(inRange_hsv,(3,3))

        canny_img = cv2.Canny(average_val_img,128,255,3)

        _,contours, hierarchy = cv2.findContours(canny_img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        try:
            for i in range(len(contours)):
                # if (len(contours[i])>self.fea_p[2]) and (len(contours[i])<self.fea_p[3]):
                # if (len(contours[i])>self.fea_p[2]):
                if (len(contours[i])>35):
                
                    min_rect = cv2.minAreaRect(contours[i])

  
                    if condition_index == 1:

                        result = (min_rect[1][0]>35 and min_rect[1][1]>35)and(abs(min_rect[1][0]-min_rect[1][1])<25)
                    elif condition_index == 2:
                        result = (min_rect[1][0] * min_rect[1][1]) > 670

                    # if (min_rect[1][0]>35 and min_rect[1][1]>35)and(abs(min_rect[1][0]-min_rect[1][1])<25):
                    # if ((min_rect[1][0] * min_rect[1][1]) > 670):
                    if result:
 
                        box_points = cv2.boxPoints(min_rect)

                        cv2.circle(img,(int(min_rect[0][0]),int(min_rect[0][1])) ,2,(self.rect_rgb[0],self.rect_rgb[1], self.rect_rgb[2]),4)
                        cv2.drawContours(img, [np.int0(box_points)], 0, (self.rect_rgb[0],self.rect_rgb[1], self.rect_rgb[2]), 2)        
                        
               
                        temp_tar_info["center"].insert(temp_num,np.int0(min_rect[0]))
                        temp_tar_info["angle"].insert(temp_num,np.int0(min_rect[2]))  

                        temp_num = temp_num + 1

            temp_tar_info["num"]=temp_num

            self.tar_info.clear()
            self.tar_info = temp_tar_info
            # print(self.tar_info)
        except:
            print("error------------->")

        return img,inRange_hsv


    def get_tar_info(self):
        pass
    
    pass

def get_pic():
    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        raise Exception("Could not open video device")
    ret, frame = video_capture.read()
    video_capture.release()
    im = trim_image(frame[:,:,::-1])
    return im

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
    func(dexarm)
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
    while current.count(True) > 1:
        img = video.get_img(1)[:,:,::-1]
        img = trim_image(img)
        av_pixel = get_av_pixel(img)
        current.pop(0)
        current.append(is_pink(av_pixel))

    end = time.perf_counter()
    # print(av_pixel)
    # dexarm.conveyor_belt_stop()
    # plt.imshow(img)
    # plt.show()
    # dexarm.conveyor_belt_forward(8300)
    elapsed = end - start
    dist = elapsed*71.0
    length = (400 - dist)/25.4
    # print(length)
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
    elif 5.5 < length < 7:
        print("4x6 Panel")
        t = (length - 6)*25.4/71
        if t > 0:
            time.sleep(t)
        func = draw_46[test_type] 
        align_panel(dexarm, func)
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
        time.sleep(1.6) # test time for 4x12
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
    move_sample(current[:3], pile_loc, dexarm_2)
    if size is not None:
        all_same(dexarm, test_type, size)
    else:
        find_length(dexarm, test_type)


def is_pink(av_pixel):
    total = sum(av_pixel)/3
    if total > 251:
        #print('filter')
        return True
    rm, rs = 190.1140793035982, 64.62080070511523
    gm, gs = 121.38619329631166, 54.87398367095535
    bm, bs = 157.78315867205592, 47.83189991536432
    new_pixel = np.array([(av_pixel[0] - rm)/rs, (av_pixel[1] - gm)/gs, (av_pixel[2] - bm)/bs])
    result = loaded_model.predict(new_pixel.reshape(1, -1)) 
    return result == 'Pink'


if __name__ == "__main__":
    dexarm.go_home()
    dexarm_2.go_home()
    dexarm.conveyor_belt_forward(8300)
    print("Ready to go")
    dexarm.fast_move_to(0, 280, 150)
    dexarm_2.fast_move_to(0, 280, 150)
    pile_loc = (-245, 0, -110)
    num_panels = int(input('How many panels?: '))
    test_type = int(input('Press 1 for cross pattern, 2 for vertical, 3 for angled, and 4 for horizontal: '))
    same_size = int(input('Press 1 if all panels same size, otherwise 2: '))
    if same_size == 1:
        size = int(input('Press 1 for all 3x5, 2 for all 4x6, 3 for all 4x8, 4 for all 4x12: '))
    for i in range(num_panels):
        if same_size == 1:
            run_test(dexarm, dexarm_2, pile_loc, test_type - 1, size - 1) 
        else:
            run_test(dexarm, dexarm_2, pile_loc, test_type - 1)
    time.sleep(3)
    dexarm.conveyor_belt_stop()
