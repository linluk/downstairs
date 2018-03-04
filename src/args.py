import argparse
import os

DEFAULT_CONFIG_FILE = os.path.expanduser('.roguelikerc')

# optionen als global zum zugreifen per args.blaaahhh

_parser = argparse.ArgumentParser()
_parser.add_argument("-c", "--commandline", action="store_true", help="termninal mode (beware of 'ncurses')")
_parser.add_argument("-a", "--ascii", action="store_true", help="tiles but allmost all ASCII")
_parser.add_argument('-f', '--config-file', default=DEFAULT_CONFIG_FILE, type=str, help='the config file')
# needs to be done
# parser.add_argument("-t", "--tiles", action="store_true", help="tiles of awesome colors, get your sunglasses with UV-Filter ready")
_args = _parser.parse_args()

cmdln_mode = _args.commandline
ascii_mode = _args.ascii
config_file = _args.config_file

if cmdln_mode == ascii_mode:
  cmdln_mode = False
  ascii_mode = True


if __name__ == '__main__':
    print(_args.commandline)
