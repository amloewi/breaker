#!/anaconda3/bin/python

# WHAT SHOULD MY SHEBANG LINE LOOK LIKE?
import os
import pygame
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


def minigame():

#    print('hello!')
#    return
#    pygame.init()
#    return
    pygame.init()
    # screen = pygame.display.set_mode((canvas_width, canvas_height))
    # surface = pygame.Surface((canvas_width, canvas_width))
    font = pygame.font.SysFont('Helvetica', 30)

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

            if time.time() > start + 31: # 5 half-periods; start+end down
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

            # And HERE, I print the correlation between
            # pressed and derivative
            # cor = round(corrcoef(pressed, derivatives)[0, 1], 2)
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
    # return
    pygame.display.quit()




if __name__=='__main__':
    minigame()
