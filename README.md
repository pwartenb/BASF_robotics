# BASF Robotics

Files used to automate film thickness test. Uses two rotrics arm one equipped with vacuum pump other has probe. Camera is mounter across from arm that has the probe. Camera is used to calculate panel length, which determines where probe is to take measurements. In order to determine length camera senses color difference between panel and pink tape uses KNN. Input of KNN is RGB pixel average of image and outputs panel or not panel. Second arm loads and unloads panels from conveyor belt. Controlled using a raspbery pi.

User Guide:

    1. open terminal
    
    2. type command: cd /Downloads/BASF_robotics and press enter
    
    3. type python3 Robot_control.py and press enter
    
    4. Input number of panels and test type press enter and robot is ready to go 
    
    5. A few common errors are with the serial ports if is says there is a communication error
    or that the serial port is busy type python3 Robot_control.py and press enter
    
    6. Another common error is a unable to open port no such file or directory.
    
    7. In this case open the Robot_control.py file and change the serial port it is connected to.
    
    8. To find the correct port open a new terminal type cd /dev enter and then ls enter. Look fir the ports 
    that start with ttyA. Common names are ttyACM0, ttyACM1, ttyACM2, or ttyAMA0.
    
    9. A third error is if the two arms collide with each other in this case press control c to kill the program 
    and flip the ports that the arms are connected to.
    
