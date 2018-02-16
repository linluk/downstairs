import typing

import pygame
from pygame.locals import *

import time

import defs

SIZE_OFFSET_X = 12
SIZE_OFFSET_Y = 12

# Color definitions, todo convert them from ui_curses to rgb
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

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
_message = pygame.Surface((defs.MESSAGE_W, defs.MESSAGE_H))  # init message surface
_line = pygame.Surface((400, 12))  # showing inputs from user when ':'

_kbc = {  # keyboard codes -> _kbc dictionary for differs in pygame and ncurses keycodes
  K_RETURN: ord('\n'),
  K_DELETE: ord('\b'),
  K_COLON:  ord(':'),
}

_tileset = {}  # dictionary for rendered tilesets


def start():
  global _screen
  global _font
  pygame.init()
  pygame.font.init()
  _font = pygame.font.SysFont('Comic Sans MS', 20)  # pixel size ???
  _screen = pygame.display.set_mode((800, 400))  # per char 10x10
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
        # _kbc dictionary for differs in pygame and ncurses keycodes
        return _kbc.get(event.key, event.key)
    time.sleep(0.01)

    # TODO: dictionary von surfaces bei erstem mal dazufügen dann muss man nicht jedesmal rendern
    # auslagern in eigene Klasse


def addch(x, y, ch, fg=WHITE, bg=BLACK, style=NORMAL):
  global _screen
  global _font
  global _tileset
  # render(text, antialias, color, background=None)
  # a dictionary of rendered tiles, so i just render every tile once
  if not ch in _tileset:
    tile_surface = _font.render(ch, True, fg)
    _tileset.update({ch: tile_surface})
  # This creates a new surface with text already drawn onto it. 
  # At the end you can just blit the text surface onto your screen.
  # blit(source, dest, area=None, special_flags = 0)
  _screen.blit(_tileset[ch], (x * SIZE_OFFSET_X, y * SIZE_OFFSET_Y))


def clear():
  global _screen
  _screen.fill((0, 0, 0))  # fill screen with black color
  # if _message is not None: # TODO: messaging system implement
  #   message(_message)

  # TODO: getline implementieren in pygame kommt aus command.py


def getline():
  global _screen
  line = ''
  drawline('::')
  while True:
    for event in pygame.event.get():
      if event.type == KEYDOWN:
        if event.key == K_RETURN:
          drawline('')
          return line
        elif event.key == K_0:
          line = line[:-1]
          drawline(line)
        else:
          line += chr(event.key)
          drawline(line)
    time.sleep(0.01)
  # win = curses.newwin(defs.INPUT_H, defs.INPUT_W, defs.INPUT_Y, defs.INPUT_X)
  # curses.curs_set(1)
  # txtbox = curses.textpad.Textbox(win)
  # line = txtbox.edit().strip()
  # win.clear() # this is not needed! or is it?
  # del win
  # curses.curs_set(0)
  # _screen.touchwin()
  # return line


def drawline(line):
  global _screen
  global _line
  _line.fill(BLACK)
  if line != '':
    _line = _font.render(line, True, WHITE)
    _screen.blit(_line, (0, 20))
  pygame.display.update()


def message(msg):
  global _screen
  global _message
  _message.fill(BLACK)
  _message = _font.render(msg, True, WHITE)
  # if msg is None:
  _screen.blit(_message, (defs.MESSAGE_X, defs.MESSAGE_Y))
  # _screen.addnstr(defs.MESSAGE_Y, defs.MESSAGE_X, ' ' * defs.MESSAGE_W, defs.MESSAGE_W - 1)
  # else:
  # _screen.addnstr(defs.MESSAGE_Y, defs.MESSAGE_X, msg, defs.MESSAGE_W - 1)
  # _message = msg


def stats(line):
  global _screen
  # _screen.addstr(defs.STATS_Y, defs.STATS_X, line)


# this section only for testing
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
