import sys
import os
from random import choice, seed

class WallSwapper:

    GNOME_3_COMMAND = '/usr/bin/gsettings set org.gnome.desktop.background picture-uri file://{0}'

    def __init__(self, img_dir):
        '''Constructor. Loads all images in img_dir into the queue.'''
        seed()
        self.verbose = False
        self.img_dir = img_dir
        self.file_list = self.getFileList()
        self.queue = self.getImageList(self.file_list)
        self.viewed = []

    def nextWallpaper(self):
        '''Sets the wallpaper to a random image in the queue. If the queue has
        been exhausted, or if changes have occured in the image directory, the 
        queue is refreshed.'''

        current_file_list = self.getFileList()

        # If a file has been added or deleted in the image directory, update
        # the queue to reflect the change, while preserving already viewed 
        # backgrounds.
        if self.file_list != current_file_list:
            if self.verbose: print('Change detected in image directory!')
            current_image_list = self.getImageList(current_file_list)
            self.queue = [img for img in current_image_list if img not in self.viewed]
            self.file_list = current_file_list

        # Check if the quue has been exhausted. If so, reset it.
        if not len(self.queue):
            if self.verbose: print('All images have been displayed. Resetting.')
            self.queue = self.getImageList(self.file_list)
            self.viewed = []
        
        # Choose a wallpaper and update the sets
        next_wallpaper = choice(self.queue)
        self.queue.remove(next_wallpaper)
        self.viewed.append(next_wallpaper)

        # Change the wallpaper
        command = self.GNOME_3_COMMAND.format(os.path.join(self.img_dir, next_wallpaper))
        os.system(command)

        if self.verbose: print('Changed wallpaper to {0}.'.format(next_wallpaper))

    def getFileList(self):
        '''Returns a list of the files in img_dir.'''

        try:
            if self.verbose: print('Reading image directory.')
            file_list = os.listdir(self.img_dir)
        except OSError as e:
            message = 'Error reading directory "{0}". Exiting. '
            if self.verbose: message += e
            print(message.format(self.img_dir))
            sys.exit(0)

        return file_list

    def getImageList(self, file_list):
        '''Returns a list of all images in file_list.'''
        imgs = []

        for file in file_list:
            if self.isImage(file):
                imgs.append(file)
                if self.verbose: print('Added {0} to available wallpaper list.'.format(file))
            else:
                if self.verbose: print('{0} is not an image. Skipping.').format(file)

        return imgs

    def isImage(self, file):
        '''Returns True if file has a recognized image extension.
        A nice improvement would be to use mimetypes instead.'''

        IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif')
        extension = os.path.splitext(file)[1]
        return (extension.lower() in IMAGE_EXTENSIONS)

    def setVerbose(self):
        '''Enables verbosity. Verbosity refers to a state of the program in
        which all actions, decisions, and errors are exhaustively enumerated 
        via standard output. The benefits to be gained from opting for such a
        deluge of information can only be realized in cases where the inspection
        of the inner workings of the program is of vital importance, such as
        debugging. Generally, one desires the suppression of this veritable 
        onslaught of minutia, because let's face it, most of us don't want
        to read so much unnecessary output diarrhea.'''
        self.verbose = True
