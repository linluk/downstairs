import argparse
import os

DEFAULT_KEYMAP = os.path.expanduser('keymap')


_parser = argparse.ArgumentParser()
_parser.add_argument("-c", "--commandline", action="store_true", help="termninal mode (beware of 'ncurses')")
_parser.add_argument("-a", "--ascii", action="store_true", help="tiles but allmost all ASCII")
# needs to be done
# parser.add_argument("-t", "--tiles", action="store_true", help="tiles of awesome colors, get your sunglasses with UV-Filter ready")
_parser.add_argument('-k', '--keymap', default=DEFAULT_KEYMAP, type=str, help='the keymap file')
_args = _parser.parse_args()

cmdln_mode = _args.commandline
ascii_mode = _args.ascii
keymap = _args.keymap

if cmdln_mode == ascii_mode:
  cmdln_mode = False
  ascii_mode = True


if __name__ == '__main__':
    print(_args.commandline)
