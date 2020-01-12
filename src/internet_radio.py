#!/usr/bin/python
import time
import threading
import asyncio
import os
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
# from lcdThread import lcdThread
from mpc_control import mpc_control

mpc = mpc_control()
#task1 = ''
#task2 = ''
# t1 = lcdThread('Thread 1') 

#try:
event_loop = asyncio.get_event_loop()

def pressed(channel):
    GPIO.remove_event_detect(channel)
    task1.cancel()
    task2.cancel()


    console_logger('reset-Edge detected on channel %s'%channel)

    #t1.restart()
    try:
        
        mpc.nextTrack()
        #await mpc.playCurrentStation()

        resettask = event_loop.create_task(mpc.playCurrentStation()
        event_loop.run_until_complete(resettask)

        console_logger('Switched to next station')
    except:
        error_handler('Error')

    GPIO.add_event_detect(gpio_input, GPIO.RISING, callback=pressed,   bouncetime=300)

async def init():
    await display('Starting radio.', 0)
    await mpc.playCurrentStation()

    # try:
    event_loop.run_until_complete(task1)
    console_logger('Program starting.')
    GPIO.add_event_detect(gpio_input, GPIO.RISING, callback=pressed,   bouncetime=300)
    
    # init()
    # while True:
    #     time.sleep(10)
        
# except KeyboardInterrupt:
#     console_logger('Program terminated nicely.')

async def displayCurrentSong():
    counter=0
    threshold=100
    currentSong = ''

    while True:
        try:
            console_logger('Fetching song')
            song = mpc.getCurrentSong()
            if(song == currentSong):
                console_logger('Same song')
                counter=counter+1
                if(counter > threshold):
                    error_handler('Too long. Restarting...')
                    mpc.stop()
                    mpc.play()

            elif(song != None):
                counter=0
                currentSong = song
                await display(song, 1, True)
        except: 
            error_handler('Unable to display song')
        
        await asyncio.sleep(5)

 

async def displayCurrentStation():
    currentStation = ''

    while True:
        try:
            mpc.connect()
            current = getCurrentStation()
            newCurrentStation = current['station']
            print(newCurrentStation)
            if(newCurrentStation == currentStation):
                console_logger('Same station')
            elif(currentStation != None):
                console_logger('New station')
                console_logger(newCurrentStation)
                await display(newCurrentStation, 0)
                currentStation = newCurrentStation

        except: 
            error_handler('Unable to fetch station name')

        await asyncio.sleep(10)

if __name__ == "__main__":
    run_app = asyncio.ensure_future(init())
    #event_loop = asyncio.get_event_loop()

    task1 = event_loop.create_task(displayCurrentStation())
    task2 = event_loop.create_task(displayCurrentSong())

    # try:
    event_loop.run_until_complete(task1)
    event_loop.run_until_complete(task2)
    # except asyncio.CancelledError:
    #     pass
    
    event_loop.run_forever()
