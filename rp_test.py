#from pitop import Pitop
from pitop import miniscreen
from time import sleep

ms = miniscreen
print(ms)
m = ms.Miniscreen()
print(m)

up = miniscreen.UpButton

down = miniscreen.DownButton

select = miniscreen.SelectButton

cancel = miniscreen.CancelButton
# define (def) actions for each of the buttons

def up_action():
    print ("UP is pressed")

def down_action():
    print ("DOWN is pressed")

def select_action():
    print ("SELECT is pressed")

def cancel_action():
    print ("CANCEL is pressed")

# Now, the algorithm
while True:
    up.when_pressed = up_action
    down.when_pressed = down_action
    select.when_pressed = select_action
    cancel.when_pressed = cancel_action
#sleep(5)