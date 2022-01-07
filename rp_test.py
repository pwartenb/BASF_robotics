import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM) # Use physical pin numbering

switch1 = 5
switch2 = 6
# switch3 = 20
# switch4 = 21

GPIO.setup(switch1, GPIO.IN)
GPIO.setup(switch2, GPIO.IN)
# GPIO.setup(switch3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# GPIO.setup(switch4, GPIO.IN, pull_up_down=GPIO.PUD_UP)