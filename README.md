# wallswapper

Creates a slideshow of your desktop background by randomly cycling through an image directory.

### Usage

    wallswapper [-h] [-d] [-i N] [-r] [-v] [--version] wallpaper_dir
    
    positional arguments:
      wallpaper_dir       your wallpaper directory
    
    optional arguments:
      -h, --help          show this help message and exit
      -d, --daemonize     TODO - run as a daemon (fork to background)
      -i N, --interval N  interval between swaps in seconds, default 300
      -r, --recurse       recurse into subdirectories of wallpaper_dir
      -v, --verbose       read about the program's inner workings
      --version           show program's version number and exit
      
