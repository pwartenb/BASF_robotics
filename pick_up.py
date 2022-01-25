from pydexarm import Dexarm
import time


def move_sample(current, obj_loc, dexarm):
    '''
    Given current location and locatoin of an obj
    Uses vaccum pump attachment to retrieve object 
    and bring it to current location
    '''
    above_obj = (obj_loc[0], obj_loc[1], 70)
    behind_obj = (obj_loc[0] + 35, obj_loc[1], 70)
    dexarm.set_module_type(2)
    dexarm.fast_move_to(*above_obj)
    dexarm.fast_move_to(*obj_loc)
    dexarm.soft_gripper_place()
    dexarm.fast_move_to(*above_obj)
    dexarm.fast_move_to(*behind_obj)
    dexarm.fast_move_to(0, 285, 60)
    dexarm.fast_move_to(0, 285, 25)
    dexarm.soft_gripper_nature()
