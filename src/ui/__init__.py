import args

if args.cmdln_mode:
  from .ui_curses import *
if args.ascii_mode:
  from .ui_pygame import *
