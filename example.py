from pydexarm import Dexarm
import time

'''windows'''
#dexarm = Dexarm(port="COM67")
'''mac & linux'''
dexarm = Dexarm(port="/dev/ttyACM0")

def blank_white(deexarm):
    dexarm.go_home()
    dexarm.fast_move_to(80, 285, 0)
    dexarm.fast_move_to(80, 285, -33)
    dexarm.fast_move_to(80, 285, 0)
    dexarm.fast_move_to(-92, 285, 0)
    dexarm.fast_move_to(-92, 285, -32)
    dexarm.fast_move_to(-92, 285, 0)
    dexarm.go_home()

def red_marks(dexarm):
    dexarm.go_home()
    dexarm.fast_move_to(65, 235, 0)
    dexarm.fast_move_to(65, 235, -32)
    dexarm.fast_move_to(65, 235, 0)
    dexarm.fast_move_to(65, 315, 0)
    dexarm.fast_move_to(65, 315, -32)
    dexarm.fast_move_to(65, 315, 0)
    dexarm.go_home()

# #dexarm.soft_gripper_nature()
# dexarm.set_module_type(2)
# #dexarm.go_home()
# # dexarm.fast_move_to(340, 0, 150)
# # dexarm.fast_move_to(0, 340, 150)
# dexarm.fast_move_to(0, 340, 150)
# dexarm.fast_move_to(0, 270, 150)
# dexarm.fast_move_to(0, 270, 30)
# dexarm.soft_gripper_place()
# dexarm.fast_move_to(340, 0, 150)
# time.sleep(7)
# dexarm.fast_move_to(0, 270, 150)
# dexarm.fast_move_to(0, 270, 30)
# time.sleep(2)
# dexarm.soft_gripper_nature()


dexarm.go_home()
print(dexarm.get_current_position())
dexarm.fast_move_to(50,0,50)


'''DexArm sliding rail Demo'''

# dexarm.conveyor_belt_forward(8300)
# time.sleep(2.5)
# dexarm.conveyor_belt_stop()

# red_marks(dexarm)

# dexarm.conveyor_belt_backward(8300)
# time.sleep(2.5)
# dexarm.conveyor_belt_stop()


'''DexArm sliding rail Demo'''

# dexarm.go_home()
# dexarm.sliding_rail_init()
# dexarm.move_to(None,None,None,0)
# dexarm.move_to(None,None,None,100)
# dexarm.move_to(None,None,None,50)
# dexarm.move_to(None,None,None,200)

dexarm.close()