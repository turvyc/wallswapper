import sys
import os
import random
import time
import argparse

class WallpaperSwitcher:

    GNOME_3_COMMAND = '/usr/bin/gsettings set org.gnome.desktop.background picture-uri file://{0}'

    IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif')

    def __init__(self, img_dir):
        random.seed()
        self.verbose = false
        self.img_dir = img_dir
        self.file_list = getFileList(img_dir)
        self.wallpapers = getImageSet(self.file_list)
        self.viewed = set()

    def nextWallpaper(self, ):
        current_file_list = getFileList(self.img_dir)

        if self.file_list != current_file_list:
            if self.verbose: print('Change detected in image directory!')
            self.wallpapers = getImageSet(current_file_list) - self.viewed

        if len(self.wallpapers) == 0:
            if self.verbose: print('All images viewed. Resetting.')
            self.wallpapers = getImageSet(current_file_list)
            self.viewed = set()
        
        new_wallpaper = random.choice(self.wallpapers)
        self.wallpapers.remove(new_wallpaper)
        self.viewed.add(new_wallpaper)

        command = GNOME_3_COMMAND.format(os.path.join(self.img_dir, new_wallpaper))
        os.system(command)

        if self.verbose: print('Changed wallpaper to {0}.').format(new_wallpaper)

    def getFileList(self, img_dir):
        try:
            if self.verbose: print('Reading image directory.')
            file_list = os.listdir(img_dir)
        except OSError as e:
            message = 'Error reading directory {0}. Exiting. '
            if self.verbose: message += e
            raise OSError(message.format(img_dir))

        return file_list

    def getImageSet(self, file_list):
        imgs = set()

        for file in file_list:
            if isImage(file):
                imgs.add(file)
                if self.verbose: print('Added {0} to available wallpaper set.').format(file)
            else:
                if self.verbose: print('{0} is not an image. Skipping.').format(file)

        return imgs

    def isImage(self, file):
        extension = os.path.splitext(file)[1]
        return (extension.lower() in self.IMAGE_EXTENSIONS)

    def setVerbose(self):
        self.verbose = true
