'''
Test file for using built in buttons
on the raspberry pi
'''
from pitop import Pitop
from time import sleep

miniscreen = Pitop().miniscreen

up = miniscreen.up_button
down = miniscreen.down_button
select = miniscreen.select_button
cancel = miniscreen.cancel_button

# define (def) actions for each of the buttons

def up_action():
    print ("UP is pressed")

def down_action():
    print ("DOWN is pressed")

def select_action():
    print ("SELECT is pressed")

def cancel_action():
    print ("CANCEL is pressed")
while True:
    up.when_pressed = up_action
    down.when_pressed = down_action
    select.when_pressed = select_action
    cancel.when_pressed = cancel_action
sleep(5)