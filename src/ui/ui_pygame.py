
import typing

import pygame
from pygame.locals import *

import time

import defs

SIZE_OFFSET_X = 12
SIZE_OFFSET_Y = 12

# Color definitions, todo convert them from ui_curses to rgb
WHITE = (255, 255, 255)
BLACK = (0, 0 ,0)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 255, 255)
BLUE = (0, 0, 255)
VIOLET = (255, 255, 255)
CYAN = (255, 255, 255)
GRAY = (180, 180, 180)
LIGHT_RED = (255, 255, 255)
LIGHT_GREEN = (255, 255, 255)
YELLOW = (255, 255, 255)
LIGHT_BLUE = (255, 255, 255)

BOLD = 0

# just for compiling
NORMAL = 1

_screen = None
_font = None

_kbc = { # keyboard codes
  K_RETURN: ord('\n')
}

def start():
  global _screen
  global _font
  pygame.init()
  pygame.font.init()
  _font = pygame.font.SysFont('Comic Sans MS', 20) # pixel size ???
  _screen = pygame.display.set_mode((800, 400)) #per char 10x10
  pygame.display.set_caption('Roguelike')

# pygame should cleanup their stuff on their own, even the most
# modules have a quit() function to do so.

def stop():
  pygame.quit()

# returns the strings of keys, like "up", "left", "j" and so on
# you could use also the pygame.key.get_pressed() but i'm
# not sure if that works here
def getch():
  pygame.display.update()
  # pygame.event.clear()
  while True:
    for event in pygame.event.get():
      if event.type == QUIT:
        return 27
      elif event.type == KEYDOWN:
        #if event.key == K_DOWN:
        return _kbc.get(event.key, event.key)
    time.sleep(0.01)

def addch(x, y, ch, fg=WHITE, bg=BLACK, style=NORMAL):
  global _screen
  global _font
  # render(text, antialias, color, background=None)
  text_surface = _font.render(ch, True, fg)
  # This creates a new surface with text already drawn onto it. 
  # At the end you can just blit the text surface onto your screen.
  # todo maybe first draw all on text_surface and then own def for blit
  # blit(source, dest, area=None, special_flags = 0)
  _screen.blit(text_surface, (x*SIZE_OFFSET_X, y*SIZE_OFFSET_Y))

def clear():
  global _screen
  _screen.fill((0, 0, 0)) # fill screen with black color
  # if _message is not None: # todo messaging system implement
  #   message(_message)

def message(msg):
  global _screen
  global _message
  #if msg is None:
    # _screen.addnstr(defs.MESSAGE_Y, defs.MESSAGE_X, ' ' * defs.MESSAGE_W, defs.MESSAGE_W - 1)
  # else:
    # _screen.addnstr(defs.MESSAGE_Y, defs.MESSAGE_X, msg, defs.MESSAGE_W - 1)
  # _message = msg

if __name__ == '__main__':
  try:
    start()
    clear()
    # addch(1, 0, 'can change colors: {}'.format(curses.can_change_color()), style=BOLD)
    addch(1, 1, 'default')
    addch(1, 2, 'red, black, bold', RED, BLACK, BOLD)
    addch(1, 3, 'green gray', GREEN, GRAY)
    """
    for i in range(0, curses.COLORS):
      curses.init_pair(i + 1, i, curses.COLOR_BLACK)
    try:
      for i in range(0, curses.COLORS):
        _screen.addstr(str(i + 1) + ' ', curses.color_pair(i))
    except curses.ERR:
      pass
    """
    _screen.getch()
  finally:
    stop()

