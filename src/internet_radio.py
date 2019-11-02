#!/usr/bin/python
import time
import threading
#import Adafruit_CharLCD as LCD
from RPLCD import CharLCD
from mpd import MPDClient
from pprint import pprint as p
import RPi.GPIO as GPIO
import traceback
from lcd_functions import *
from config import *
from db import *
from utils import *
from lcdThread import lcdThread
from mpc_control import mpc_control

mpc = mpc_control()
t1 = lcdThread('Thread 1') 

try:
    def pressed(channel):
        GPIO.remove_event_detect(channel)

        console_logger('reset-Edge detected on channel %s'%channel)

        t1.restart()
        try:
            mpc.nextTrack()
            mpc.playCurrentStation()

            console_logger('Switched to next station')
        except:
            error_handler('Error')

        GPIO.add_event_detect(gpio_input, GPIO.RISING, callback=pressed,   bouncetime=300)

    def init():
        display('Starting radio.', 0)
        mpc.playCurrentStation()
        t1.start() 

    console_logger('Program starting.')
    GPIO.add_event_detect(gpio_input, GPIO.RISING, callback=pressed,   bouncetime=300)
    
    init()
    while True:
        time.sleep(10)
        
except KeyboardInterrupt:
    console_logger('Program terminated nicely.')
