from time import time, sleep

def distance(trigger, echo):    
    # set Trigger to HIGH
    GPIO.output(trigger, True)

    # set Trigger after 0.01ms to LOW
    sleep(0.00001)
    GPIO.output(trigger, False)

    StartTime = time()
    StopTime = time()

    # save StartTime
    while GPIO.input(echo) == 0:
        StartTime = time()

    # save time of arrival
    while GPIO.input(echo) == 1:
        StopTime = time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-e', '--echo', type=int, default=17, help='number of ECHO pin, default 17')
parser.add_argument('-t', '--trigger', type=int, default=27, help='number of TRIGGER pin, default 27')
args = parser.parse_args()

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)  # BOARD or BCM
GPIO.setup(args.trigger, GPIO.OUT)
GPIO.setup(args.echo, GPIO.IN)

try:
    while True:
        dist = distance(trigger=args.trigger, echo=args.echo)
        print (f'Measured Distance = {dist:.1f} cm')
        sleep(1)
except KeyboardInterrupt:
    print("Measurement stopped by User")
    GPIO.cleanup()
