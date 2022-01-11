from pydexarm import Dexarm
import time


def move_sample(current, obj_loc, dexarm):
    '''
    Given current location and locatoin of an obj
    Uses vaccum pump attachment to retrieve object 
    and bring it to current location
    '''
    above_current = (current[0], current[1], current[2]+75)
    above_obj = (obj_loc[0], obj_loc[1], obj_loc[2]+75)
    dexarm.set_module_type(2)
    dexarm.fast_move_to(*above_obj)
    dexarm.fast_move_to(*obj_loc)
    dexarm.soft_gripper_place()
    dexarm.fast_move_to(*above_obj)
    dexarm.fast_move_to(*above_current)
    dexarm.fast_move_to(*current)
    dexarm.soft_gripper_nature()
