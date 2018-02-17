
TITLE = 'Roguelike'
AUTHOR = 'Lukas Singer, Daniel Nimmervoll'
EMAIL = 'lukas42singer (at) gmail (dot) com'
COPYRIGHT = 'Copyright (C) 2018 by {}'.format(AUTHOR)
CREDITS = [
    "https://www.python.org/",
    "https://vim.sourceforge.io/",
    "http://www.roguebasin.com/",
    ""]

# the whole screen size
SCREEN_X = 0
SCREEN_Y = 0
SCREEN_W= 80
SCREEN_H= 40

# the message area
MESSAGE_X = 0
MESSAGE_Y = 1
MESSAGE_W = SCREEN_W - MESSAGE_X
MESSAGE_H = 1

# the input area
INPUT_X = 0
INPUT_Y = MESSAGE_Y + MESSAGE_H
INPUT_W = SCREEN_W - INPUT_X
INPUT_H = 1

STATS_X = 0
STATS_Y = SCREEN_H - 3
STATS_W = SCREEN_W
STATS_H = 2

# the level area
LEVEL_X = 0
LEVEL_Y = INPUT_Y + INPUT_H + 1
LEVEL_W = SCREEN_W - LEVEL_X
LEVEL_H = SCREEN_H - LEVEL_Y - STATS_H



