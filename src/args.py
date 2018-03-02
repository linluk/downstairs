import argparse

# optionen als global zum zugreifen per args.blaaahhh

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--commandline", action="store_true", help="termninal mode (beware of 'ncurses')")
parser.add_argument("-a", "--ascii", action="store_true", help="tiles but allmost all ASCII")
# needs to be done
# parser.add_argument("-t", "--tiles", action="store_true", help="tiles of awesome colors, get your sunglasses with UV-Filter ready")
args = parser.parse_args()

if args.commandline == args.ascii:
  args.commandline = False
  args.ascii = True


if __name__ == '__main__':
  print(args.commandline)
