from pydexarm import Dexarm
import time

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

def vert_35(dexarm):
    '''
    Only input is dexarm instance returns nothing
    Takes film thickness measurements at all 7
    required spots for 4x6 Ford panel
    '''
    time.sleep(0.45)
    dexarm.conveyor_belt_stop()
    take_sample(dexarm, (41, 245, -40)) # calls take sample with specified location
    take_sample(dexarm, (14, 270, -40))
    take_sample(dexarm, (-10 + 14, 270, -40))
    take_sample(dexarm, (-20 + 14, 270, -40))
    take_sample(dexarm, (-30 + 14, 270, -40))
    take_sample(dexarm, (-40 + 14, 270, -40))
    take_sample(dexarm, (41, 294, -40))
    dexarm.fast_move_to(0, 280, 150) # return to starting position

def vert_46(dexarm):
    '''
    Only input is dexarm instance returns nothing
    Takes film thickness measurements at all 7
    required spots for 4x6 Ford panel
    '''
    time.sleep(0.45)
    dexarm.conveyor_belt_stop()
    take_sample(dexarm, (41, 250, -40)) # calls take sample with specified location
    take_sample(dexarm, (0, 280, -40))
    take_sample(dexarm, (-10, 280, -40))
    take_sample(dexarm, (-20, 280, -40))
    take_sample(dexarm, (-30, 280, -40))
    take_sample(dexarm, (-40, 280, -40))
    take_sample(dexarm, (41, 312, -40))
    dexarm.fast_move_to(0, 280, 150) # return to starting position

def vert_48(dexarm):
    '''
    Only input is dexarm instance returns nothing
    Takes film thickness measurements at all 7
    required spots for 4x6 Ford panel
    '''
    time.sleep(.9)
    dexarm.conveyor_belt_stop()
    take_sample(dexarm, (75, 250, -40))
    take_sample(dexarm, (0, 280, -40))
    take_sample(dexarm, (-10, 280, -40))
    take_sample(dexarm, (-20, 280, -40))
    take_sample(dexarm, (-30, 280, -40))
    take_sample(dexarm, (-40, 280, -40))
    take_sample(dexarm, (75, 312, -40))
    dexarm.fast_move_to(0, 280, 150) # return to starting position

def vert_412(dexarm):
    time.sleep(1.9)
    dexarm.conveyor_belt_stop()
    take_sample(dexarm, (146, 250, -40))
    take_sample(dexarm, (5, 280, -40))
    take_sample(dexarm, (-5, 280, -40))
    take_sample(dexarm, (-15, 280, -40))
    take_sample(dexarm, (-25, 280, -40))
    take_sample(dexarm, (-35, 280, -40))
    take_sample(dexarm, (146, 312, -40))
    dexarm.fast_move_to(0, 280, 150) # return to starting position

def horiz_46(dexarm):
    '''
    Only input is dexarm instance returns nothing
    Takes film thickness measurements at all 7
    required spots for 4x6 Ford panel
    '''
    time.sleep(0.45)
    dexarm.conveyor_belt_stop()
    take_sample(dexarm, (41, 250, -40)) # calls take sample with specified location
    take_sample(dexarm, (-20, 320 - 60, -40))
    take_sample(dexarm, (-20, 330 - 60, -40))
    take_sample(dexarm, (-20, 340 - 60, -40))
    take_sample(dexarm, (-20, 350 - 60, -40))
    take_sample(dexarm, (-20, 360 - 60, -40))
    take_sample(dexarm, (41, 312, -40))
    dexarm.fast_move_to(0, 280, 150) # return to starting position

def horiz_48(dexarm):
    '''
    Only input is dexarm instance returns nothing
    Takes film thickness measurements at all 7
    required spots for 4x6 Ford panel
    '''
    time.sleep(.9)
    dexarm.conveyor_belt_stop()
    take_sample(dexarm, (75, 250, -40))
    take_sample(dexarm, (-20, 260, -40))
    take_sample(dexarm, (-20, 270, -40))
    take_sample(dexarm, (-20, 280, -40))
    take_sample(dexarm, (-20, 290, -40))
    take_sample(dexarm, (-20, 300, -40))
    take_sample(dexarm, (75, 312, -40))
    dexarm.fast_move_to(0, 280, 150) # return to starting position

def horiz_412(dexarm):
    time.sleep(1.9)
    dexarm.conveyor_belt_stop()
    take_sample(dexarm, (146, 250, -40))
    take_sample(dexarm, (-15, 260, -40))
    take_sample(dexarm, (-15, 270, -40))
    take_sample(dexarm, (-15, 280, -40))
    take_sample(dexarm, (-15, 290, -40))
    take_sample(dexarm, (-15, 300, -40))
    take_sample(dexarm, (146, 312, -40))
    dexarm.fast_move_to(0, 280, 150) # return to starting position

def cross_35(dexarm):
    '''
    Only input is dexarm instance returns nothing
    Takes film thickness measurements at all 7
    required spots for 4x6 Ford panel
    '''
    time.sleep(0.45)
    dexarm.conveyor_belt_stop()
    take_sample(dexarm, (41, 245, -40)) # calls take sample with specified location
    
    take_sample(dexarm, (-6 + 2*8.7, 260, -40))
    take_sample(dexarm, (-6 + 8.7, 265, -40))

    take_sample(dexarm, (-6, 270, -40))

    take_sample(dexarm, (-6 - 8.7, 265, -40))
    take_sample(dexarm, (-6 - 2*8.7, 260, -40))

    take_sample(dexarm, (-6 + 8.7, 275, -40))
    take_sample(dexarm, (-6 + 2*8.7, 280, -40))

    take_sample(dexarm, (-6 - 8.7, 275, -40))
    take_sample(dexarm, (-6 - 2*8.7, 280, -40))

    take_sample(dexarm, (41, 294, -40))
    dexarm.fast_move_to(0, 280, 150) 

def cross_46(dexarm):
    '''
    Only input is dexarm instance returns nothing
    Takes film thickness measurements at all 7
    required spots for 4x6 Ford panel
    '''
    time.sleep(0.45)
    dexarm.conveyor_belt_stop()
    take_sample(dexarm, (41, 250, -40)) # calls take sample with specified location
    
    take_sample(dexarm, (-20 + 2*8.7, 270, -40))
    take_sample(dexarm, (-20 + 8.7, 275, -40))

    take_sample(dexarm, (-20, 280, -40))

    take_sample(dexarm, (-20 - 8.7, 275, -40))
    take_sample(dexarm, (-20 - 2*8.7, 270, -40))

    take_sample(dexarm, (-20 + 8.7, 285, -40))
    take_sample(dexarm, (-20 + 2*8.7, 290, -40))

    take_sample(dexarm, (-20 - 8.7, 285, -40))
    take_sample(dexarm, (-20 - 2*8.7, 290, -40))

    take_sample(dexarm, (41, 312, -40))
    dexarm.fast_move_to(0, 280, 150) # return to starting position

def cross_48(dexarm):
    time.sleep(.9)
    dexarm.conveyor_belt_stop()
    take_sample(dexarm, (75, 250, -40))
    
    take_sample(dexarm, (-20 + 2*8.7, 270, -40))
    take_sample(dexarm, (-20 + 8.7, 275, -40))

    take_sample(dexarm, (-20, 280, -40))

    take_sample(dexarm, (-20 - 8.7, 275, -40))
    take_sample(dexarm, (-20 - 2*8.7, 270, -40))

    take_sample(dexarm, (-20 + 8.7, 285, -40))
    take_sample(dexarm, (-20 + 2*8.7, 290, -40))

    take_sample(dexarm, (-20 - 8.7, 285, -40))
    take_sample(dexarm, (-20 - 2*8.7, 290, -40))

    take_sample(dexarm, (75, 312, -40))
    dexarm.fast_move_to(0, 280, 150) # return to starting position

def cross_412(dexarm):
    time.sleep(1.9)
    dexarm.conveyor_belt_stop()
    take_sample(dexarm, (146, 250, -40))
    
    take_sample(dexarm, (-15 + 2*13, 265, -40))
    take_sample(dexarm, (-15 + 13, 272.5, -40))

    take_sample(dexarm, (-15, 280, -40))

    take_sample(dexarm, (-15 - 2*13, 265, -40))
    take_sample(dexarm, (-15 - 13, 272.5, -40))

    take_sample(dexarm, (-15 + 13, 287.5, -40))
    take_sample(dexarm, (-15 + 2*13, 295, -40))

    take_sample(dexarm, (-15 - 13, 287.5, -40))
    take_sample(dexarm, (-15 - 2*13, 295, -40))

    take_sample(dexarm, (146, 312, -40))
    dexarm.fast_move_to(0, 280, 150) # return to starting position

def angle_46(dexarm):
    '''
    Only input is dexarm instance returns nothing
    Takes film thickness measurements at all 7
    required spots for 4x6 Ford panel
    '''
    time.sleep(0.45)
    dexarm.conveyor_belt_stop()
    take_sample(dexarm, (41, 250, -40)) # calls take sample with specified location
    take_sample(dexarm, (-55 + 60, 320 - 60, -40))
    take_sample(dexarm, (-55 + 60, 330 - 60, -40))
    take_sample(dexarm, (-55 + 60, 340 - 60, -40))
    take_sample(dexarm, (-55 + 60, 350 - 60, -40))
    take_sample(dexarm, (-55 + 60, 360 - 60, -40))

    take_sample(dexarm, (2*8.7 - 60, 270, -40))
    take_sample(dexarm, (8.7 - 60, 275, -40))
    take_sample(dexarm, (-60, 280, -40))
    take_sample(dexarm, (-8.7 - 60, 285, -40))
    take_sample(dexarm, (-2*8.7 - 60, 290, -40))

    take_sample(dexarm, (41, 312, -40))
    dexarm.fast_move_to(0, 280, 150) # return to starting position

def angle_48(dexarm):
    time.sleep(.9)
    dexarm.conveyor_belt_stop()
    take_sample(dexarm, (75, 250, -40))

    take_sample(dexarm, (-56 + 55, 260, -40))
    take_sample(dexarm, (-56 + 55, 270, -40))
    take_sample(dexarm, (-56 + 55, 280, -40))
    take_sample(dexarm, (-56 + 55, 290, -40))
    take_sample(dexarm, (-56 + 55, 300, -40))

    take_sample(dexarm, (4 + 2*8.7 - 55, 270, -40))
    take_sample(dexarm, (4 + 8.7 - 55, 275, -40))
    take_sample(dexarm, (4 - 55, 280, -40))
    take_sample(dexarm, (4 - 8.7 - 55, 285, -40))
    take_sample(dexarm, (4 - 2*8.7 - 55, 290, -40))

    take_sample(dexarm, (75, 312, -40))
    dexarm.fast_move_to(0, 280, 150) # return to starting position

def angle_412(dexarm):
    time.sleep(1.9)
    dexarm.conveyor_belt_stop()
    take_sample(dexarm, (146, 250, -40))

    take_sample(dexarm, (-15 - 57  + 75, 260, -40))
    take_sample(dexarm, (-15 - 57  + 75, 270, -40))
    take_sample(dexarm, (-15 - 57  + 75, 280, -40))
    take_sample(dexarm, (-15 - 57  + 75, 290, -40))
    take_sample(dexarm, (-15 - 57  + 75, 300, -40))

    take_sample(dexarm, (3 + 2*13 - 75, 265, -40))
    take_sample(dexarm, (3 + 13 - 75, 272.5, -40))
    take_sample(dexarm, (3, 280 - 75, -40))
    take_sample(dexarm, (3 - 13 - 75, 287.5, -40))
    take_sample(dexarm, (3 - 2*13 - 75, 295, -40))

    take_sample(dexarm, (146, 312, -40))
    dexarm.fast_move_to(0, 280, 150) # return to starting position