
import typing

import pygame
from pygame.locals import *

import defs

# Color definitions, todo convert them from ui_curses to rgb
WHITE = (255, 255, 255)
BLACK = (0, 0 ,0)

RED = (255, 255, 255)
GREEN = (255, 255, 255)
ORANGE = (255, 255, 255)
BLUE = (255, 255, 255)
VIOLET = (255, 255, 255)
CYAN = (255, 255, 255)
GRAY = (255, 255, 255)
LIGHT_RED = (255, 255, 255)
LIGHT_GREEN = (255, 255, 255)
YELLOW = (255, 255, 255)
LIGHT_BLUE = (255, 255, 255)

# just for compiling
NORMAL = 1

_screen = None
_font = None

def start():
  global _screen
  global _font
  pygame.init()
  pygame.font.init()
  _font = pygame.font.SysFont('Comic Sans MS', 12) # pixel size ???
  _screen = pygame.display.set_mode((800, 600)) #per char 10x10
  pygame.display.set_caption('Roguelike')

# pygame should cleanup their stuff on their own, even the most
# modules have a quit() function to do so.

def stop():
  pass

# returns the strings of keys, like "up", "left", "j" and so on
# you could use also the pygame.key.get_pressed() but i'm
# not sure if that works here
def getch():
  for event in pygame.event.get():
    return event.type

def addch(x, y, ch, fg=WHITE, bg=BLACK, style=NORMAL):
  global _screen
  global _font
  # render(text, antialias, color, background=None)
  text_surface = _font.render(ch, False, fg, bg)
  # This creates a new surface with text already drawn onto it. 
  # At the end you can just blit the text surface onto your screen.
  # todo maybe first draw all on text_surface and then own def for blit
  # blit(source, dest, area=None, special_flags = 0)
  _screen.blit(text_surface, (x, y))

def clear():
  global _screen
  _screen.fill((0, 0, 0)) # fill screen with black color
  # if _message is not None: # todo messaging system implement
  #   message(_message)




