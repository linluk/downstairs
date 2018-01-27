
import typing

import curses
import curses.textpad # type: ignore

import defs


BLACK = 0
RED = 1
GREEN = 2
ORANGE = 3
BLUE = 4
VIOLET = 5
CYAN = 6
WHITE = 7
GRAY = 8
LIGHT_RED = 9
LIGHT_GREEN = 10
YELLOW = 11
LIGHT_BLUE = 12

NORMAL = 0
BOLD = curses.A_BOLD

_screen = None
_message = None



_color_pairs = {} # type: typing.Dict[typing.Tuple[typing.Any, typing.Any], typing.Any]
_color_pair_idx = 1
def _color(fg, bg):
  global _color_pairs
  global _color_pair_idx
  k = (fg, bg)
  if k in _color_pairs:
    return _color_pairs[k]
  curses.init_pair(_color_pair_idx, fg, bg)
  cp = curses.color_pair(_color_pair_idx)
  _color_pair_idx += 1
  _color_pairs[k] = cp
  return cp



def start():
  global _screen
  _screen = curses.initscr()
  curses.start_color()
  curses.noecho()
  curses.cbreak()
  curses.curs_set(0)
  # uncomment next line to disallow CTRL-C as exception
  #curses.raw()
  _screen.timeout(-1)


def stop():
  global _screen
  curses.nocbreak()
  curses.echo()
  curses.endwin()
  _screen = None

def getch():
  global _screen
  return _screen.getch()

def addch(x, y, ch, fg=WHITE, bg=BLACK, style=NORMAL):
  global _screen
  _screen.addstr(y, x, ch, _color(fg, bg) | style)

def clear():
  global _screen
  global _message
  _screen.clear()
  if _message is not None:
    message(_message)

def getline():
  global _screen
  win = curses.newwin(defs.INPUT_H, defs.INPUT_W, defs.INPUT_Y, defs.INPUT_X)
  curses.curs_set(1)
  txtbox = curses.textpad.Textbox(win)
  line = txtbox.edit().strip()
  #win.clear() # this is not needed! or is it?
  del win
  curses.curs_set(0)
  _screen.touchwin()
  return line

def message(msg):
  global _screen
  global _message
  if msg is None:
    _screen.addnstr(defs.MESSAGE_Y, defs.MESSAGE_X, ' ' * defs.MESSAGE_W, defs.MESSAGE_W - 1)
  else:
    _screen.addnstr(defs.MESSAGE_Y, defs.MESSAGE_X, msg, defs.MESSAGE_W - 1)
  _message = msg

def stats(line):
  global _screen
  _screen.addstr(defs.STATS_Y, defs.STATS_X, line)


if __name__ == '__main__':
  try:
    start()
    clear()
    addch(1, 0, 'can change colors: {}'.format(curses.can_change_color()), style=BOLD)
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


