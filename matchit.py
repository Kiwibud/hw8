# ----------------------------------------------------------------------
# Name:        matchit
# Purpose:     Implement a single player matching game
#
# Author: Kiwibud
# ----------------------------------------------------------------------
"""
A single player matching game.

usage: matchit.py [-h] [-f] {blue,green,magenta} image_folder
positional arguments:
  {blue,green,magenta}  What color would you like for the player?
  image_folder          What folder contains the game images?

optional arguments:
  -h, --help            show this help message and exit
  -f, --fast            Fast or slow game?
"""
import tkinter
import os
import random
import argparse


class MatchGame(object):
    """
    GUI Game class for a matching game.

    Arguments:
    parent: the root window object
    player_color (string): the color to be used for the matched tiles
    folder (string) the folder containing the images for the game
    delay (integer) how many milliseconds to wait before flipping a tile

    Attributes:
    Please list ALL the instance variables here
    """

    # Add your class variables if needed here - square size, etc...)
    SQUARE_SIZE = 150
    NUM_GRIDS = 4
    CANVAS_SIZE = SQUARE_SIZE * NUM_GRIDS + 100
    score = 100
    num_of_tries = 0
    pic = []
    default_color = 'yellow'

    def __init__(self, parent, player_color, folder, delay):
        parent.title('Match it!')
        self.color = player_color
        self.delay = delay
        self.folder = folder
        self.image_id = []
        # Initiate list of images
        self.new_list = get_image_list(folder) * 2
        random.shuffle(self.new_list)
        # Initialize self.sammy
        self.sammy = tkinter.PhotoImage(file=os.path.join(self.folder,
                                                          self.new_list[0]))
        print(self.new_list)  # to check the 16 images in random order
        # Create the restart button widget
        restart_btn = tkinter.Button(parent, text='RESTART', width=20,
                                     command=self.restart)
        restart_btn.grid()
        # Create a canvas widget
        self.canvas = tkinter.Canvas(parent, width=self.CANVAS_SIZE,
                                     height=self.CANVAS_SIZE)
        # create the grid on canvas
        self.create_grid()
        self.canvas.grid()
        # self.pic = tkinter.PhotoImage(
        #     file=os.path.join(folder, self.new_list[x_iter]))
        # img_id = self.canvas.create_image(self.SQUARE_SIZE / 2,
        #                                   self.SQUARE_SIZE / 2,
        #                                   image=self.pic)
        # self.image_id.append(img_id)
        self.canvas.bind("<Button-1>", self.play)
        # Create a label widget for the score and end of game messages
        self.score_label = tkinter.Label(parent, text=f'Score: {self.score}',
                                         borderwidth=1)
        self.score_label.grid()
        # Create any additional instance variable you need for the game

    def restart(self):
        """
        This method is invoked when player clicks on the RESTART button.
        It shuffles and reassigns the images and resets the GUI and the
        score.
        :return: None
        """
        self.score = 100
        self.num_of_tries = 0
        for tile in self.canvas.find_all():
            self.canvas.itemconfigure(tile, fill=self.default_color)
        # random.shuffle(get_image_list(folder))

    def play(self, event):
        """
        This method is invoked when the user clicks on a square.
        It implements the basic controls of the game.
        :param event: event (Event object) describing the click event
        :return: None
        """
        tile = self.canvas.find_closest(event.x, event.y)
        tile_id = tile[0] - 1
        print(tile)  # tile id, eg (1,) when click the first square
        # self.select(tile)  # to create the tag for tile
        cords = self.canvas.coords(tile)  # coordinates of tile
        print(os.path.join(self.folder, self.new_list[tile_id]))
        self.sammy = tkinter.PhotoImage(file=os.path.join(self.folder,
                                        self.new_list[tile_id]))
        print(cords)
        self.image_id = self.canvas.create_image((cords[0] + cords[2])/2,
                                                 (cords[1] + cords[3])/2,
                                                 image=self.sammy)
        self.canvas.after(self.delay, self.disappear, tile)

    def create_grid(self):
        for y_iter in range(self.NUM_GRIDS):
            for x_iter in range(self.NUM_GRIDS):
                x, y = x_iter * self.SQUARE_SIZE, y_iter * self.SQUARE_SIZE
                x_stop, y_stop = x + self.SQUARE_SIZE, y + self.SQUARE_SIZE
                self.canvas.create_rectangle(x, y, x_stop, y_stop,
                                             outline=self.color,
                                             fill=self.default_color)

    def disappear(self, tile):
        """
        Remove Sammy's image from the Canvas
        Call appear to have the image reappear after a delay
        :return: None
        """
        self.canvas.delete(self.image_id)
        self.canvas.itemconfigure(tile, fill=self.default_color)

    def select(self, event):
        """
        Tag the clicked tile as selected/unselected
        :param tile:
        :return: None
        """
        
        tile = self.canvas.find_withtag(tkinter.CURRENT)
        self.canvas.itemconfigure(tile, tag="selected")
#         if "selected" in self.canvas.gettags(tile):
#             # print("unselected")
#             self.canvas.itemconfigure(tile, tag="unselected")
#         else:
#             # print("selected")
#             self.canvas.itemconfigure(tile, tag="selected")


def get_arguments():
    """
    Parse and validate the command line arguments
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('color', help='What color would you like for the '
                                      'player?',
                        choices=['blue', 'green', 'magenta'])
    parser.add_argument('image_folder', help='Folder contains images',
                        type=file_type)
    parser.add_argument('-f', '--fast', help='Fast or slow game',
                        action='store_true')
    arguments = parser.parse_args()
    color = arguments.color
    image_folder = arguments.image_folder
    fast = arguments.fast
    return color, image_folder, fast


def file_type(dir):
    """
    Validate if the folder exists and contains at least 8 gif files
    :param folder:
    :return:
    """
    path, folder = os.path.split(dir)
    if path == '':
        path = '.'
    # check if the folder is in the directory
    if folder not in os.listdir(path):
        raise argparse.ArgumentTypeError(f'{folder} is not a valid folder')
    else:
        # check if it contains at least 8 gif files
        if len(get_image_list(folder)) < 8:
            raise argparse.ArgumentTypeError(f'{folder} must contain at '
                                             f'least 8 gif images')
    return folder


def get_image_list(folder):
    image_list = []
    for each_file in os.listdir(folder):
        filename, ext = os.path.splitext(each_file)
        if ext == '.gif':
            image_list.append(each_file)
    return image_list


def main():
    # Retrieve and validate the command line arguments using argparse
    delay_time = 3000
    color, image_folder, fast = get_arguments()
    if fast:
        delay_time = 1000
    # Instantiate a root window
    root = tkinter.Tk()
    # Instantiate a MatchGame object with the correct arguments
    MatchGame(root, color, image_folder, delay_time)
    # Enter the main event loop
    root.mainloop()


if __name__ == '__main__':
    main()

