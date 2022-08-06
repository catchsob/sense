from hcsr04 import HCSR04
from time import sleep

YOUR_TRIGGER = 0
YOUR_ECHO = 1

sensor = HCSR04(trigger_pin=YOUR_TRIGGER, echo_pin=YOUR_ECHO, echo_timeout_us=10000)
try:
    while True:
        print(f'Distance: {sensor.distance_cm()}cm')
        sleep(1)
except OSError as e:
    print('ERROR getting distance:', e)