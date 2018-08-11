# import rumps
import os
import sys
import keyboard
# import pygame
import tkinter as tk
import time
import math
import random
# from math import sqrt

from tkinter import Tk, Canvas, PhotoImage, mainloop

# from waves import minigame
# from pynput import keyboard
# rumps.debug_mode(True)

# pyinstaller Breaker.py --windowed --onefile # This works! Onefile shrinks size (???)
# This call => 'UPX is available,' but the file was no smaller than above;
# still need to sort the issue of, maybe I'm still getting all of conda, despite being
# in a separate environment? Confusing.
# pyinstaller Breaker.py --windowed --onefile --upx-dir=/usr/local/bin/
# adding --onedir makes the .app file explode again
# https://github.com/pyinstaller/pyinstaller/issues/2270
# IF I -- conda install -c conda-forge numpy (NOT pip install numpy, w/in env)
# THEN IT'S 25MB, because (?) THIS version of numpy (WITHIN the conda env)
# does NOT require this massive set of MKL libraries (which are maybe an error).
# HOWEVER -- the .app also quits immediately.
# Wish I knew why!



canvas_width=1000 #308
canvas_height=400

freq = 2
amplitude = 90
speed = .25



def pearson(series_1, series_2):
    # Takes in a list of pairwise ratings and produces a pearson similarity

    sum1 = sum(series_1)
    sum2 = sum(series_2)

    squares1 = sum([ n*n for n in series_1 ])
    squares2 = sum([ n*n for n in series_2 ])

    product_sum = sum([ n * m for n,m in zip(series_1, series_2) ])

    size = len(series_1)

    numerator = product_sum - ((sum1 * sum2)/size)
    denominator = sqrt((squares1 - (sum1*sum1) / size) * (squares2 - (sum2*sum2)/size))

    if denominator == 0:
        return 0

    return numerator/denominator



# Used to store debug file
#import os
#BASE_DIR = os.path.realpath(os.path.dirname(__file__))


def sine_wave_anim():

    # Update sine wave
    frequency = 4
    amplitude = 50 # in px
    speed = 1

    # We create a blank area for what where we are going to draw
    color_table = [["#000000" for x in range(0, canvas_width)] for y in range(0, amplitude*2)]

    # And draw on that area
    for x in range(0, canvas_width):
        y = int(amplitude + amplitude*math.sin(frequency*((float(x)/canvas_width)*(2*math.pi) + (speed*time.time()))))
        color_table[y][x] = "#ffff00"

        # Don't individually put pixels as tkinter sucks at this
        #img.put("#ffff00", (x, y))

    # Then batch put it on the canvas
    # tkinter is extremely inefficient doing it one by one
    img.put(''.join("{" + (" ".join(str(color) for color in row)) + "} " for row in color_table), (0, int(canvas_height/2 - amplitude)))

    # Debug the color_table
    #with open(os.path.join(BASE_DIR, 'output.txt'), "w+") as text_file:
    #   text_file.write(''.join("{" + (" ".join(str(color) for color in row)) + "} " for row in color_table))


    # Continue the animation as fast as possible. A value of 0 (milliseconds), blocks everything.
    window.after(100, sine_wave_anim)





if __name__ == "__main__":

#    try:
    # keyboard.add_hotkey('windows+shift+y', set_flag) #lambda:print('hello!')) #set_flag)

    # os.environ['SDL_VIDEO_CENTERED'] = '1' # didn't work; below DID (SORT of; only x-axis)
    # OR COULD JUST MAKE IT FILL THE SCREEN, WHICH I WANT TO DO ANYWAY => (0, 0) is CORRECT
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 0) # ... finding SCREEN width etc.
    # OR, call this at the beginning of the GAME, TOO?

    # Some config width height settings
    canvas_width = 640
    canvas_height = 480

    # Create a window
    window = Tk()
    # Set the window title
    window.wm_title("Sine Wave")

    # Put a canvas on the window
    canvas = Canvas(window, width=canvas_width, height=canvas_height, bg="#000000")
    canvas.pack()

    # Create a image, this acts as the canvas
    img = PhotoImage(width=canvas_width, height=canvas_height)

    # Put the image on the canvas
    canvas.create_image((canvas_width/2, canvas_height/2), image=img, state="normal")


    # Start off the anim
    sine_wave_anim()
    mainloop()
