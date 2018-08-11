#!/usr/bin/python

# import rumps
import os
import sys
import keyboard
import pygame
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
# ... also, this stopped being true at some point. I think. Still issues.
# BUT WHATEVER, also, um, the hotkey doesn't work, when running the .app!

# Piece re: correct installation of SMALL numpy, but maybe don't need at ALL!
# https://github.com/pyinstaller/pyinstaller/issues/2270

# Switched to python=3.6.6 because there was a 3.7 issue with pyinstaller
# https://github.com/pyinstaller/pyinstaller/issues/3642

# import pygame
import time
import math
import random
# from numpy import corrcoef
from math import sqrt


canvas_width=1000 #308
canvas_height=400

sin_color = pygame.Color(255,0,0) # or nothing
red = pygame.Color(255,0,0)
white = pygame.Color(255, 255, 255)
background_color = pygame.Color(0,0,0) # or 'black'

freq = 2
amplitude = 90
speed = .25

BREAKER = pygame.USEREVENT + 1


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


def any_key_to_continue(text, screen, surface, font):

    # should really adjust, based on rect size, for the text
    # BUT NOW, RUN
    surface.fill(background_color)
    screen.blit(surface, (0, 0)) # render surface on canvas
    screen.blit(font.render(text, True, [255]*3), (450, 150))
    pygame.display.flip() # update the rendered objects

    # Press any key to continue
    while True:
        # If there's a 'for' AND a 'while,' you only 'break' out of ONE
        if any([e.type == pygame.KEYDOWN for e in pygame.event.get()]):
            break


def set_flag():
    """Puts an event in the pygame events queue to start the minigame
    """
    my_event = pygame.event.Event(BREAKER, message="Breathe in...")
    pygame.event.post(my_event)
    print('posted!')


def minigame(font):
    """

    Does NOT initialize the game;
    """

    # Need to PUT IT AT THE FRONT OF THE STACK
    # (is this necessary, HERE? It's already outside of the function)
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 0) # ... finding SCREEN width etc.
    # screen = pygame.display.set_mode((canvas_width, canvas_height))
    # surface = pygame.Surface((canvas_width, canvas_width))

    # pygame.FULLSCREEN APPEARS TO SOLVE THE PROBLEM OF FOCUS;
    # when I trigger this, it just -- fills the screen! automatic!
    screen = pygame.display.set_mode((canvas_width, canvas_height), pygame.FULLSCREEN)
    surface = pygame.Surface((1000, 400), pygame.FULLSCREEN)

    for game_number in range(1, 4): # In case there's a bug, quit after 3 rounds

        any_key_to_continue("Breathe in...", screen, surface, font)

        pressed = []
        derivatives = []

        start = time.time()
        while True:

            # Necessary for the animation
            surface.fill(background_color)
            # A vertical line at mid-way
            for i in range(canvas_height):
                surface.set_at((int(canvas_width/2), i), white)

            if time.time() > start + 31:  # 5 half-periods; start+end down
                break

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    return

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                sin_color = red
                pressed.append(True)
            else:
                sin_color = white
                pressed.append(False)

            y0 = 0
            for x in range(canvas_width):
                y = int((canvas_height/2) + 270
                        + amplitude*math.sin(freq*((float((x - 100) % canvas_width)/canvas_width) * (2 * math.pi)
                        + (speed * (time.time()-start))) + 270) - 270)

                # Calculates a simple 1-lag derivative AT THE CENTERPOINT
                if x==int(canvas_width/2):
                    derivatives.append(y - y0)

                y0 = y

                surface.set_at((x, y), sin_color) # sets a single pixel

            cor = pearson(pressed, derivatives)

            screen.blit(surface, (0, 0)) # render surface on canvas
            # screen.blit(font.render(str(cor), False, [255]*3), (20, 20))
            pygame.display.flip() # update the rendered objects

        # Outside of the 'while' (one ROUND of the game)
        if cor > 0.5 or game_number==3:
            break
        else:
            any_key_to_continue("One more time.", screen, surface, font)

    # Outside of the 'for' (successfully COMPETED the game)
    surface.fill(background_color)
    any_key_to_continue("Ok.", screen, surface, font)
    any_key_to_continue("Ready?", screen, surface, font)
    any_key_to_continue("Get to it.", screen, surface, font)

    screen = pygame.display.set_mode((1, 1))
    surface = pygame.Surface((1, 1))
    # return
    # pygame.display.quit()

def start():
    # os.environ['SDL_VIDEO_CENTERED'] = '1' # didn't work; below DID (SORT of; only x-axis)
    # OR COULD JUST MAKE IT FILL THE SCREEN, WHICH I WANT TO DO ANYWAY => (0, 0) is CORRECT
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 0) # ... finding SCREEN width etc.
    # OR, call this at the beginning of the GAME, TOO?
    pygame.init() # THESE DO NOT WORK (with WHICH VERSION?)
    pygame.mixer.quit() # Don't know if this makes any difference, but -- not BAD!
    screen = pygame.display.set_mode((1, 1))
    surface = pygame.Surface((1, 1))
    font = pygame.font.SysFont('Helvetica', 30)

    while True:
        event = pygame.event.wait()#get() # THIS MIGHT HAVE FIXED IT!
        # for event in events:
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == BREAKER:
            print('triggered!')
            minigame(font) # only piece that needs to be passed. Huh.
    # except Exception as x:
        # with ('breakerlog.txt', 'w') as f:
            # f.write(str(x))


if __name__ == "__main__":

#    try:
    # NECESSARY BECAUSE OF THE HOTKEY
    # https://stackoverflow.com/questions/23108335/how-to-run-a-python-script-inside-applescript
    # (Got me to add 'python' in the osa call)
    # os.system("""osascript -e 'do shell script "<commands go here>" ' with administrator privileges'""")
    # PROBABLY
    # 1) find the application
    # https://stackoverflow.com/questions/1724693/find-a-file-in-python
    def find(name, path):
        for root, dirs, files in os.walk(path):
            if name in files:
                return os.path.join(root, name)
    # app_path = find('Breaker.app', '/') # right?
    # 2) run with the VERSION OF PYTHON THAT'S INSIDE.
    # right_python = os.path.join(app_path, 'bin/python') # or whatever
    # path = "{} {}".format(right_python, app_path)
    # OR, do I do "sudo open Breaker.app"; how does that conflict with it having
    # ALREADY --BEEN-- called by 'open'?
    # https://stackoverflow.com/questions/3170771/mac-os-x-python-gui-administrator-prompt
    # os.system("""osascript -e 'do shell script "{}" with administrator privileges'""".format(path))

    if False:
        from tkinter import simpledialog, Tk # One of the ones where you can't tk.f
        root = Tk()
        root.withdraw()
        pwd = simpledialog.askstring("Breaker", "Breaker needs your password!", show='*', parent=root)
        root.destroy()

        script = """from minigame import minigame; import keyboard; keyboard.add_hotkey("windows+shift+y", minigame)"""
        os.system(""" echo {} | sudo -S python3 -c '{}'""".format(pwd, script))
    else:
        keyboard.add_hotkey('windows+shift+y', set_flag) #lambda:print('hello!')) #set_flag)


    # print(pwd)
    # but what is this RUNNING?
    # keyboard.add_hotkey('windows+shift+y', set_flag) #lambda:print('hello!')) #set_flag)

    # from tkinter import *
    #
    # def getpwd():
    #     password = ''
    #     root = Tk()
    #     pwdbox = Entry(root, show = '*')
    #     def onpwdentry(evt):
    #          password = pwdbox.get()
    #          root.destroy()
    #     def onokclick():
    #          password = pwdbox.get()
    #          root.destroy()
    #     Label(root, text = 'Password').pack(side = 'top')
    #
    #     pwdbox.pack(side = 'top')
    #     pwdbox.bind('<Return>', onpwdentry)
    #     Button(root, command=onokclick, text = 'OK').pack(side = 'top')
    #
    #     root.mainloop()
    #     return password
    #
    # print(getpwd())

    start()
