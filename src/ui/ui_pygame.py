import pygame
from pygame.locals import *

import time

import defs
from ui.gfx_tiles import Tiles

SIZE_OFFSET_X = 12
SIZE_OFFSET_Y = 16

FONT_SIZE = 14

# Color definitions, todo convert them from ui_curses to rgb
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 161, 0)
BLUE = (20, 39, 209)
VIOLET = (86, 20, 209)
CYAN = (15, 156, 216)
GRAY = (100, 100, 100)
LIGHT_RED = (247, 103, 134)
LIGHT_GREEN = (104, 216, 128)
YELLOW = (247, 225, 32)
LIGHT_BLUE = (66, 116, 255)

BOLD = 0

MESSAGE_RECT = defs.MESSAGE_W * SIZE_OFFSET_X, defs.MESSAGE_H * SIZE_OFFSET_Y

# just for compiling
NORMAL = 1

_screen = None
_font = None
_message = pygame.Surface(MESSAGE_RECT)  # init message surface
_line = pygame.Surface((400, 12))  # showing inputs from user when ':'
_stati_line = pygame.Surface((defs.SCREEN_W * SIZE_OFFSET_X, 20))
_msg = None

_kbc = {  # keyboard codes -> _kbc dictionary for differs in pygame and ncurses keycodes
    K_RETURN: ord('\n'),
    K_DELETE: ord('\b'),
    K_COLON: ord(':'),
}

_tileset = {}  # dictionary for rendered tilesets


def start():
    global _screen
    global _font
    global _tiles
    pygame.init()
    pygame.font.init()
    _font = pygame.font.SysFont('Deja Vu Sans Mono', FONT_SIZE)  # pixel size ???
    _screen = pygame.display.set_mode((defs.SCREEN_W * SIZE_OFFSET_X, defs.SCREEN_H * SIZE_OFFSET_Y))
    # load the sprites
    # _tiles = Tiles(_screen, u"res/Redjack17.png", 17, 0)  # tile class
    # _tiles.get_tiles()
    pygame.display.set_caption('LinLuk')  # Lindström Liker


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
        # start message line
        all_keys = pygame.key.get_pressed()
        if all_keys[pygame.K_PERIOD] and (all_keys[pygame.K_LSHIFT] or all_keys[pygame.K_RSHIFT]):
            return ord(':')

        time.sleep(0.01)

        # TODO: dictionary von surfaces bei erstem mal dazufügen dann muss man nicht jedesmal rendern
        # auslagern in eigene Klasse


def addch(x, y, ch, fg=WHITE, bg=BLACK, style=NORMAL):
    global _screen
    global _font
    global _tileset  # dict
    global _tiles  # surfaces
    # render(text, antialias, color, background=None)
    # a dictionary of rendered tiles, so i just render every tile once
    # AHHH didnt work because if rendered it only once it keeps the color
    # and the far more distant tiles are not grayed anymore
    # if not ch in _tileset:
    # possibility to use graphic tiles instead of rendered fonts
    # elif ch == '.':
    #  tile_surface = _tiles.tiles[(7, 14)]
    # else:
    tile_surface = _font.render(ch, True, fg, bg)
    # grphic tiles instead of rendered font
    # if ch == '#':
    #   tile_surface = _tiles.tiles[(13, 11)]
    # elif ch == '.':
    #   tile_surface = _tiles.tiles[(2, 14)]
    _tileset.update({ch: tile_surface})
    # This creates a new surface with text already drawn onto it.
    # At the end you can just blit the text surface onto your screen.
    # blit(source, dest, area=None, special_flags = 0)
    _screen.blit(_tileset[ch], (x * SIZE_OFFSET_X, y * SIZE_OFFSET_Y))


def clear():
    global _screen
    _screen.fill((0, 0, 0))  # fill screen with black color
    if _msg is not None:
        message(_msg)

    # TODO: getline implementieren in pygame kommt aus command.py


def getline():
    global _screen
    global old_line
    line = '::'
    drawline(line)
    pygame.event.clear()
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    drawline(line, True)  # clear()
                    return line[2:]  # remove colons
                elif event.key == K_BACKSPACE:
                    line = line[:-1]
                    drawline(line)
                else:
                    line += chr(event.key)
                    drawline(line)
        time.sleep(0.01)


def drawline(line, isDone=False):
    global _screen
    global _line
    _line.fill(BLACK)
    if not isDone:
        _line = _font.render(line, True, WHITE)
    _screen.blit(_line, (5, 40))
    pygame.display.update((5, 40, pygame.display.get_surface().get_width() - 5, 20))


def draw_intro(line, x, y):
    global _screen
    #surf = pygame.Surface((defs.SCREEN_W * SIZE_OFFSET_X, defs.SCREEN_H * SIZE_OFFSET_Y))
    surf = _font.render(line, True, WHITE)
    _screen.blit(surf, (x, y))
    pygame.display.update()


def message(msg):
    global _screen
    global _message
    global _msg
    _message.fill(BLACK)
    if msg is not None:
        _message = _font.render(msg, True, LIGHT_RED)
        _screen.blit(_message, (0, 0))
    pygame.display.update((0, 0, *MESSAGE_RECT))
    _msg = msg


def stats(line):
    global _screen
    global _stati_line
    _stati_line.fill(BLACK)
    _stati_line = _font.render(line, True, WHITE)
    _screen.blit(_stati_line, (5, 20))
    pygame.display.update((defs.STATS_Y, defs.STATS_X, defs.SCREEN_W * SIZE_OFFSET_X, 20))


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
