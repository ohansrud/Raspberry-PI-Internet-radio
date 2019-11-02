from mpd import MPDClient
from utils import * 
from db import *
from lcd_functions import display

class mpc_control(): 
    def __init__(self): 
        self.client = MPDClient()
    
    def connect(self):
        try:
            self.client.ping()
        except: 
            try:
                self.client.connect("localhost", 6600)
                console_logger('Connected!')
            except:
                error_handler('Could not connect!')

    def getCurrentSong(self):
        try:
            self.connect()
            currentsong = self.client.currentsong()
            title = currentsong['title']
            return title
        except:
            error_handler('Could not fetch song!')

    def getStatus(self):
        try:
            self.connect()
            return self.client.status()
        except:
            error_handler('Could not get status!')


    def nextTrack(self):
        self.connect()
        self.client.next()
        playNext()

    def playCurrentStation(self):
        try:
            self.connect()
            current = getCurrentStation()
            self.client.stop()
            self.client.clear()
            console_logger('Playing Current stream')
            console_logger(current['stream'])
            self.client.add(current['stream'])
            self.client.play(0)
            name = current['station']
            console_logger(name)
            display(name, 0)
        except:
            error_handler('Could not play current track')
