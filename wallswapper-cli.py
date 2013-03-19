import argparse
import wallswapper
from time import sleep

version = '0.1a'
default_interval = 300 # 5 minutes

parser = argparse.ArgumentParser(prog = 'wallswapper')

parser.add_argument('wallpaper_dir', help = 'your wallpaper directory')
parser.add_argument('-i', '--interval', help = 'TODO - interval between swaps in seconds, default 300',
                   metavar = 'N', type = int, default = default_interval)
parser.add_argument('-r', '--recurse', help = 'TODO - treat wallpaper_dir recursively',
                    action = 'store_true')
parser.add_argument('-v', '--verbose', help = 'read about the program\'s inner workings', 
                    action = 'store_true')
parser.add_argument('--version', action = 'version', version = '%(prog)s ' + version)

args = parser.parse_args()

swapper = wallswapper.WallSwapper(args.wallpaper_dir)
if args.verbose:
    swapper.setVerbose()

# Every programmer's nightmare, the infinite loop! This program should ideally
# be forked (i.e. following the command with '&'), or should be written as a
# daemon with a config file.
while True:
    swapper.nextWallpaper()
    sleep(args.interval)
