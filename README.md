# BASF Robotics

Files used to automate film thickness test. Uses two rotrics arm one equipped with vacuum pump other has probe. Camera is mounter across from arm that has the probe. Camera is used to calculate panel length, which determines where probe is to take measurements. In order to determine length camera senses color difference between panel and pink tape uses KNN. Input of KNN is RGB pixel average of image and outputs panel or not panel. Second arm loads and unloads panels from conveyor belt. Controlled using a raspbery pi.

User Guide:
    
    1. Make sure both robots are turned on. A green light on the back of the bot indicates it is on.

    2. open terminal
    
    3. type command: cd /Downloads/BASF_robotics and press enter
    
    4. type python3 Robot_control.py and press enter
    
    5. Input number of panels and test type press enter and robot is ready to go 
    
Common Errors:

    1. If the robot was just turned on or if itbeing used for the first time that today
    the computer may struggle to connect iwht the robot. IF one or both of the arms does 
    not move when it should this is likely the cause. To solve this either close the terminal 
    and start again or press contorl c, which kills the program, and run python3 Robot_control.py 
    again. 
    
    2. A second common problem is when the program fails to run and throws an error that says device or
    resource busy. This is also a connenction issue that can sometimes happen when the robot was just turned on.
    If this is case run python3 Robot_control.py again. Sometimes you will hve to run the program two or three times 
    before the computer connects with the robot. 
    
Raspberry Pi Guide:

    1. Turn on by holding the power switch on the side.
    
    2. It can often take a few minutes to boot up. If a 4 appears on the screen this means it is booting up.
    
    3. If the screen displays a picture of an sd card with an arrow to a computer this means the SD card has come loose. 
    In this case remove the panel that covers the SD card, take out the SD card, and reinsert it.
