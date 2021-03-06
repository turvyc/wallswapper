import argparse
import wallswapper
from time import sleep

program_name = 'wallswapper'
version = '0.1'
default_interval = 180 # 3 minutes

parser = argparse.ArgumentParser(prog = program_name)

parser.add_argument('wallpaper_dir', help = 'your wallpaper directory')
parser.add_argument('-d', '--daemonize', help = 'TODO - run as a daemon (fork to background)',
                    action = 'store_true')
parser.add_argument('-i', '--interval', help = 'TODO - interval between swaps in seconds, default 300',
                   metavar = 'N', type = int, default = default_interval)
parser.add_argument('-r', '--recurse', help = 'recurse into subdirectories of wallpaper_dir',
                    action = 'store_true')
parser.add_argument('-v', '--verbose', help = 'read about the program\'s inner workings', 
                    action = 'store_true')
parser.add_argument('--version', action = 'version', version = '%(prog)s ' + version)

args = parser.parse_args()

swapper = wallswapper.WallSwapper(args.wallpaper_dir)

if args.verbose:
    swapper.setVerbose()

if args.recurse:
    swapper.setRecursive()

swapper.generateQueue()

# Every programmer's nightmare, the infinite loop! This program should ideally
# be forked (i.e. following the command with '&'), or should be written as a
# daemon with a config file.
while True:
    swapper.nextWallpaper()
    sleep(args.interval)
