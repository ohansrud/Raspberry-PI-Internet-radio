import threading 
import asyncio 
import time 
from utils import *
from mpc_control import *
from db import *

class lcdThread(threading.Thread): 
    def __init__(self, name): 
        threading.Thread.__init__(self) 
        self.name = name 
        self.currentSong = "."
        self.currentStation = "."      
        self.elapsed = "."
        self.mpc = mpc_control()        
    
    def watchdog(self, args):
        console_logger('Running watchdog')
        mpc_control.connect(self)
        status = self.mpc.getStatus()
        state = status['state']
        console_logger(state)
        if(state == 'stop'):
            error_handler("Playback stopped! Restarting...")
            self.mpc.playCurrentStation()

    def run(self):
        counter=0
        threshold=100

        while True:
            # try:
            #     watchdog(self)
            # except: 
            #     error_handler('Unable to run watchdog')

            try:
                self.mpc.connect()
                current = getCurrentStation()
                currentStation = current['station']
                if(currentStation == self.currentStation):
                    console_logger('Same station ' + str(counter))
                elif(currentStation != None):
                    console_logger(currentStation)
                    display(currentStation, 0)
                    self.currentStation = currentStation

            except: 
                error_handler('Unable to fetch station name')

            # try:
            #     console_logger('Fetching song')
            #     song = self.mpc.getCurrentSong()
            #     if(song == self.currentSong):
            #         console_logger('Same song')
            #         counter=counter+1
            #         if(counter > threshold):
            #             error_handler('Too long. Restarting...')
            #             self.mpc.stop()
            #             self.mpc.play()

            #     elif(song != None):
            #         counter=0
            #         self.currentSong = song
            #         display(song, 1, True)
            # except: 
            #     error_handler('Unable to display song')
            
            asyncio.sleep(5)
            