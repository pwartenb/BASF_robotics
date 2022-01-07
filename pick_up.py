from pydexarm import Dexarm
import time

dexarm = Dexarm(port="/dev/ttyACM0")

def go_get(current, obj_loc):
    above_current = (current[0], current[1], 150)
    above_obj = (obj_loc[0], obj_loc[1], 150)
    dexarm.set_module_type(2)
    #dexarm.go_home()
    dexarm.fast_move_to(*above_obj)
    dexarm.fast_move_to(*obj_loc)
    time.sleep(2)
    dexarm.soft_gripper_place()
    dexarm.fast_move_to(*above_current)
    dexarm.fast_move_to(*current)
    dexarm.soft_gripper_nature()

if __name__ == "__main__":
    num_panels = int(input('How many panels?'))
    for i in range(num_panels):
        current = (0, 270, 30)
        obj_loc = (270, 0, 30)
        go_get(current, obj_loc)