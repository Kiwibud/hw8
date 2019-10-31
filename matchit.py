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
import sys


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

    def __init__(self, parent, player_color, folder, delay):
        parent.title('Match it!')
        # Create the restart button widget
        restart = tkinter.Button(parent, text='RESTART', width=20,
                                 command=self.restart)
        restart.grid()
        # Create a canvas widget
        self.canvas = tkinter.Canvas(parent, width=self.CANVAS_SIZE,
                                     height=self.CANVAS_SIZE)
        self.canvas.grid()
        # create the grid frame on canvas
        self.create_grids(self.canvas)
        # Create a label widget for the score and end of game messages
        game_label = tkinter.Label(parent, text='Score', borderwidth=1)
        game_label.grid()
        # Create any additional instance variable you need for the game

    def restart(self):
        """
        This method is invoked when player clicks on the RESTART button.
        It shuffles and reassigns the images and resets the GUI and the
        score.
        :return: None
        """
        pass  # take out the pass statement and enter your code

    def play(self, event):
        """
        This method is invoked when the user clicks on a square.
        It implements the basic controls of the game.
        :param event: event (Event object) describing the click event
        :return: None
        """
        pass  # take out the pass statement and enter your code

    def display_score(self):
        pass  # take out the pass statement and enter your code

    def create_grids(self, parent):
        for y_iter in range(self.NUM_GRIDS):
            for x_iter in range(self.NUM_GRIDS):
                tile = tkinter.Canvas(parent, width=self.SQUARE_SIZE,
                                      height=self.SQUARE_SIZE)
                tile.create_rectangle(0, 0, self.SQUARE_SIZE, self.SQUARE_SIZE,
                                      outline='black', fill='yellow')
                tile.grid(column=x_iter, row=y_iter)

    # Enter your additional method definitions below
    # Make sure they are indented inside the MatchGame class
    # Make sure you include docstrings for all the methods.


# Enter any function definitions here to get and validate the
# command line arguments.  Include docstrings.
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


def file_type(folder):
    """
    Validate if the folder exists and contains at least 8 gif files
    :param folder:
    :return:
    """
    image_list = []
    # check if the folder is in the directory
    if folder not in os.listdir():
        raise argparse.ArgumentError()
        # print(f' Error: {folder} is not a valid folder')
    else:
        # check if it contains at least 8 gif files
        for each_file in os.listdir(folder):
            filename, ext = os.path.splitext(each_file)
            if ext == '.gif':
                image_list.append(each_file)
        print(image_list)
        if len(image_list) < 8:
            # print(f'Error:{folder} must contain at least 8 gif files')
            raise argparse.ArgumentError()
    return folder


def main():
    # Retrieve and validate the command line arguments using argparse
    delay_time = 1
    color, image_folder, fast = get_arguments()
    if fast:
        delay_time = 3
    # Instantiate a root window
    root = tkinter.Tk()
    # Instantiate a MatchGame object with the correct arguments
    match_game = MatchGame(root, color, image_folder, delay_time)
    # Enter the main event loop
    root.mainloop()
    pass  # take out the pass statement and enter your code


if __name__ == '__main__':
    main()
