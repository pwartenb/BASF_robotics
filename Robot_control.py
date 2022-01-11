import cv2
import numpy as np
import math
from matplotlib import pyplot as plt
from Cam_dev import *
from pydexarm import Dexarm
from pick_up import *
import time

'''windows'''
#dexarm = Dexarm(port="COM67")
'''mac & linux'''
dexarm = Dexarm(port="/dev/ttyACM0") # initializes dexarm to correct port

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


def recogn_main():
    video.open(0,320,240)
    revogn = Color_block_recogn(red_hsv,feature_param,rgb_param)
    return video.get_img(0)

def trim_image(im):
    '''
    takes in image and trims to only view conveyor
    belt that is directly under the camera allows 
    for more accurate sensing of panel
    '''
    list_im = list(im)
    x_start = 75
    x_end = 200
    y_start = 140
    y_end = 180
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
    total = 0
    for row in im:
        for item in row:
            av = sum(item)/3
            total += av
    return total/total_num

def take_sample(dexarm, loc):
    '''
    Takes in dexarm instance and specified 
    location return nothing
    Moves to above location and then drops 
    to accurately take sample
    '''
    above_loc = (loc[0], loc[1], loc[2] + 30)
    dexarm.fast_move_to(*above_loc)
    dexarm.fast_move_to(*loc)
    dexarm.fast_move_to(*above_loc)

def ford_46(dexarm):
    '''
    Only input is dexarm instance returns nothing
    Takes film thickness measurements at all 7
    required spots for 4x6 Ford panel
    '''
    take_sample(dexarm, (41, 309, 30)) # calls take sample with specified location
    take_sample(dexarm, (-20, 320, 30))
    take_sample(dexarm, (-20, 330, 30))
    take_sample(dexarm, (-20, 340, 30))
    take_sample(dexarm, (-20, 350, 30))
    take_sample(dexarm, (-20, 360, 30))
    take_sample(dexarm, (41, 371, 30))
    dexarm.fast_move_to(0, 340, 150) # return to starting position

def align_panel(elapsed, dexarm, func):
    '''
    Takes in time elapsed from panel passing through camera,
    a dexarm instance, and func that correlates to panel test.
    Function moves panel so samples can be taken accurately
    '''
    dexarm.conveyor_belt_backward(8300)
    time.sleep(elapsed*.8)
    dexarm.conveyor_belt_stop()
    func(dexarm)
    dexarm.dealy_s(2)
    dexarm.conveyor_belt_backward(8300)
    time.sleep(4.6)
    dexarm.conveyor_belt_stop()

def find_length(dexarm):
    '''
    Takes in Dexarm instance and time that panel began to move.
    Calculates length of panel and chooses corresponding test program
    then returns panel to mosition under vacuum pump so it can be
    placed on the done pile. Returns nothing.
    '''
    video.open(0,320,240)
    previous = "Black"
    start = 0
    while True:
        img = video.get_img(0)[:,:,::-1]
        # plt.imshow(img)
        # plt.show()
        img = trim_image(img)
        av_pixel = get_av_pixel(img)
        if av_pixel < 185:
            if previous == "White":
                end = time.perf_counter()
                elapsed = end - start
                dist = elapsed*71.5
                print("Len of panel: ", (dist/25.4), " inches")
                length = dist/25.4
                if 5.5 < length < 6.5:
                    align_panel(elapsed, dexarm, ford_46)
                    video.close()
                    break
                else:
                    previous = "Black"
                    img = video.get_img(0)[:,:,::-1]
                    img = trim_image(img)
                    av_pixel = get_av_pixel(img)
                    while av_pixel > 180:
                        img = video.get_img(0)[:,:,::-1]
                        img = trim_image(img)
                        av_pixel = get_av_pixel(img)
        else:
            if previous == "Black":
                previous = "White"
                start = time.perf_counter()
        if av_pixel < 35:
            dexarm.conveyor_belt_stop()
            video.close()
            break
    video.close()

def run_test(dexarm, dexarm_2 = 0, pile_loc = 0):
    '''
    Takes in two dexarm objects. One should have probe attached other
    has vacuum pump. Moves panels to conveyor belt and then
    calls function to find length and engage probe 
    '''
    dexarm.fast_move_to(0, 340, 150)
    # dexarm_2.fast_move_to(0, -340, 150)
    # current = dexarm_2.get_current_position()
    current = 0, 250, 30
    move_sample(current, pile_loc, dexarm)
    # dexarm.conveyor_belt_forward(8300)
    # find_length(dexarm)

if __name__ == "__main__":
    #dexarm.conveyor_belt_stop()
    print("Ready to go")
    dexarm.go_home()
    dexarm.fast_move_to(0, 340, 150)
    #dexarm_2.go_home()
    pile_loc = (-360, 0, 15)
    num_panels = int(input('How many panels?'))
    for i in range(num_panels):
        #run_test(dexarm, dexarm_2, pile_loc)
        run_test(dexarm, 0, pile_loc)
    pass
