#!/usr/bin/python
# Snake Heart
# Code Angel

import sys
import os
import pygame
from pygame.locals import *

import screen
import player_class
import monster
import map_class
import utils


# Setup
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.init()
display = screen.Display()
pygame.key.set_repeat(10, 20)
clock = pygame.time.Clock()
font = pygame.font.SysFont('Helvetica', 16)