import time
from RPLCD import CharLCD
import RPi.GPIO as GPIO
from config import *
import asyncio

lcd = CharLCD(numbering_mode=GPIO.BCM, cols=lcd_columns, rows=lcd_rows, pin_rs=lcd_rs, pin_e=lcd_en, pins_data=[lcd_d4, lcd_d5, lcd_d6, lcd_d7])

def clear_row(row):
    lcd.cursor_pos = (row, 0)
    lcd.write_string('                ')

def write_line(message, row):
    clear_row(row)
    lcd.cursor_pos = (row, 0) 
    lcd.write_string(message)

async def scroll_left(message, row, delay):
    scroll = len(message)+1
    
    for i in range(scroll):
        await asyncio.sleep(delay)
        substring = message[i:lcd_columns+i]
        write_line(substring, row)

async def display(title, row, scroll = False):
    lcd.cursor_pos = (row, 0) 

    substring = title[0:lcd_columns]
    write_line(substring, row)

    #Show for 3 seconds
    await asyncio.sleep(3)

    if(scroll):
        #Scroll left
        event_loop = asyncio.get_event_loop()

        task = event_loop.create_task(scroll_left(title, row, 0.5))
        event_loop.run_until_complete(task)

        # await scroll_left(title, row, 0.5)

        write_line(substring, row)

        #Show for 3 seconds
        await asyncio.sleep(3)