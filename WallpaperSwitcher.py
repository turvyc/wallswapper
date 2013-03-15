import sys
import os
import random
import time
import argparse

class WallpaperSwitcher:

    GNOME_3_COMMAND = '/usr/bin/gsettings set org.gnome.desktop.background picture-uri file://{0}'

    IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif')

    def __init__(self, img_dir):
        '''Constructor. Loads all images in img_dir into the queue.'''
        random.seed()
        self.verbose = false
        self.img_dir = img_dir
        self.file_list = getFileList(img_dir)
        self.queue = getImageSet(self.file_list)
        self.viewed = set()

    def nextWallpaper(self):
        '''Sets the wallpaper to a random image in the queue. If the queue has
        been exhausted, or if changes have occured in the image direcotyr, it 
        is refreshed.'''

        current_file_list = getFileList(self.img_dir)

        # If a file has been added or deleted in the image directory, update
        # the queue to reflect the change, while preserving already viewed 
        # backgrounds.
        if self.file_list != current_file_list:
            if self.verbose: print('Change detected in image directory!')
            self.queue = getImageSet(current_file_list) - self.viewed

        # Check if the quue has been exhausted. If so, reset it.
        if not len(self.queue):
            if self.verbose: print('All images viewed. Resetting.')
            self.queue = getImageSet(current_file_list)
            self.viewed = set()
        
        # Choose a wallpaper and update the sets
        next_wallpaper = random.choice(self.queue)
        self.queue.remove(next_wallpaper)
        self.viewed.add(next_wallpaper)

        # Change the wallpaper
        command = GNOME_3_COMMAND.format(os.path.join(self.img_dir, next_wallpaper))
        os.system(command)

        if self.verbose: print('Changed wallpaper to {0}.').format(next_wallpaper)

    def getFileList(self, img_dir):
        '''Returns a list of the files in img_dir.'''
        try:
            if self.verbose: print('Reading image directory.')
            file_list = os.listdir(img_dir)
        except OSError as e:
            message = 'Error reading directory {0}. Exiting. '
            if self.verbose: message += e
            raise OSError(message.format(img_dir))

        return file_list

    def getImageSet(self, file_list):
        '''Returns a set of the image files in file_list.'''
        imgs = set()

        for file in file_list:
            if isImage(file):
                imgs.add(file)
                if self.verbose: print('Added {0} to available wallpaper set.').format(file)
            else:
                if self.verbose: print('{0} is not an image. Skipping.').format(file)

        return imgs

    def isImage(self, file):
        '''Returns true if file has a recognized image extension.'''
        extension = os.path.splitext(file)[1]
        return (extension.lower() in self.IMAGE_EXTENSIONS)

    def setVerbose(self):
        '''Enables verbosity. Verbosity refers to a state of the program in
        which all actions, decisions, and errors are exhaustively enumerated 
        via standard output. The benefits to be gained from opting for such a
        deluge of information can only be realized in cases where the inspection
        of the inner workings of the program is of vital importance, such as
        debugging. Generally, one desires the suppression of this veritable 
        onslaught of minutia, because let's face it, most of us don't want
        to read so much crap.'''
        self.verbose = true
