import pygame, sys
from pygame.locals import *

SCREENWIDTH = 640
SCREENHEIGHT = 480

def blit_sprite(sprite, x, y):
    gamescreen.blit(sprite, [x, y])