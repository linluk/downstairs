from args import args

if args.commandline:
  from .ui_curses import *
if args.ascii:
  from .ui_pygame import *
