
import ui
import enum

try:
  from enum import auto
except ImportError:
  # enum.auto() is new in py3.6
  __my_enum_auto_id = 0
  def auto() -> int:
    global __my_enum_auto_id
    i = __my_enum_auto_id
    __my_enum_auto_id += 1
    return i

class Commands(enum.Enum):
  QUIT = auto()
  SKIP = auto()
  NORTH_WEST = auto()
  NORTH = auto()
  NORTH_EAST = auto()
  EAST = auto()
  SOUTH_EAST = auto()
  SOUTH = auto()
  SOUTH_WEST = auto()
  WEST = auto()
  OPEN = auto()
  TAKE = auto()
  OK = auto()

  def is_direction(self):
    return self in (Commands.NORTH_WEST, Commands.NORTH, Commands.NORTH_EAST, Commands.EAST, Commands.SOUTH_EAST, Commands.SOUTH, Commands.SOUTH_WEST, Commands.WEST)

  def direction_to_dxdy(self):
    if self == Commands.NORTH_WEST: return (-1, -1)
    elif self == Commands.NORTH: return (0, -1)
    elif self == Commands.NORTH_EAST: return (1, -1)
    elif self == Commands.EAST: return (1, 0)
    elif self == Commands.SOUTH_EAST: return (1, 1)
    elif self == Commands.SOUTH: return (0, 1)
    elif self == Commands.SOUTH_WEST: return (-1, 1)
    elif self == Commands.WEST: return (-1, 0)

    else: return None

shortcuts = {}
commands = {}

def __init_cmd(value, command, shortcut=None):
  global shortcuts
  global commands
  if shortcut is not None:
    shortcut = ord(shortcut) if isinstance(shortcut, str) else shortcut
    shortcuts[shortcut] = command
  commands[command] = value

def init_commands():
  _ = __init_cmd
  _(Commands.QUIT, 'quit', 27)
  _(Commands.SKIP, 'skip', '.')
  _(Commands.NORTH_WEST, 'north west', 'z') # TODO: this is german KB specific
  _(Commands.NORTH, 'north', 'k')
  _(Commands.NORTH_EAST, 'north east', 'u')
  _(Commands.EAST, 'east', 'l')
  _(Commands.SOUTH_EAST, 'south east', 'n')
  _(Commands.SOUTH, 'south', 'j')
  _(Commands.SOUTH_WEST, 'south west', 'b')
  _(Commands.WEST, 'west', 'h')
  _(Commands.OPEN, 'open', 'o')
  _(Commands.TAKE, 'take', 't')
  _(Commands.OK, 'ok', '\n')


def getcmd():
  global shortcuts
  global commands
  cmd = None
  while cmd == None:
    ch = ui.getch()
    st = None
    if ch == ord(':'):
      st = ui.getline()
    elif ch in shortcuts:
      st = shortcuts[ch]
    if st in commands:
      cmd = commands[st]
      ui.message(None)
    else:
      ui.message('unknown command')
  return cmd

def require_direction():
  cmd = getcmd()
  while not cmd.is_direction():
    cmd = getcmd()
  return cmd

