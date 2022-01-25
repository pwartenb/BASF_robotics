# BASF Robotics

Files used to automate film thickness test. Uses two rotrics arm one equipped with vacuum pump other has probe. Camera is mounter across from arm that has the probe. Camera is used to calculate panel length, which determines where probe is to take measurements. In order to determine length camera senses color difference between panel and pink tape uses KNN. Input of KNN is RGB pixel average of image and outputs panel or not panel. Second arm loads and unloads panels from conveyor belt. Controlled using a raspbery pi.

User Guide:
    - open terminal
    - type command: cd /Downloads/BASF_robotics and press enter
    - type Robot_control.py
