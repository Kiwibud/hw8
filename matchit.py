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
    count = 0
    pic = []

    def __init__(self, parent, player_color, folder, delay):
        parent.title('Match it!')
        # Create the restart button widget
        restart_btn = tkinter.Button(parent, text='RESTART', width=20,
                                     command=self.restart)
        restart_btn.grid()
        # Create a canvas widget
        self.canvas = tkinter.Canvas(parent, width=self.CANVAS_SIZE,
                                     height=self.CANVAS_SIZE)
        self.canvas.grid()

        self.new_list = get_image_list(folder) * 2
        random.shuffle(self.new_list)
        print(self.new_list)

        # create the grid frame on canvas
        self.image_id = []
        for y_iter in range(self.NUM_GRIDS):
            for x_iter in range(self.NUM_GRIDS):
                tile = tkinter.Canvas(self.canvas, width=self.SQUARE_SIZE,
                                      height=self.SQUARE_SIZE,
                                      background='yellow')
                tile.create_rectangle(0, 0, self.SQUARE_SIZE, self.SQUARE_SIZE,
                                      outline='black')
                self.pic = tkinter.PhotoImage(
                    file=os.path.join(folder, self.new_list[x_iter]))
                id = tile.create_image(self.SQUARE_SIZE / 2,
                                                  self.SQUARE_SIZE / 2,
                                                  image=self.pic)
                self.image_id.append(id)
                tile.grid(column=x_iter, row=y_iter)
        # self.create_grids(self.canvas)
        self.color = player_color
        self.delay = delay

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
        self.count = 0
        # random.shuffle(get_image_list(folder))

    def play(self, event):
        """
        This method is invoked when the user clicks on a square.
        It implements the basic controls of the game.
        :param event: event (Event object) describing the click event
        :return: None
        """
        pass  # take out the pass statement and enter your code

    # def create_grids(self, parent):
    #
    #     for y_iter in range(self.NUM_GRIDS):
    #         for x_iter in range(self.NUM_GRIDS):
    #             tile = tkinter.Canvas(parent, width=self.SQUARE_SIZE,
    #                                   height=self.SQUARE_SIZE,
    #                                   background='yellow')
    #             tile.create_rectangle(0, 0, self.SQUARE_SIZE, self.SQUARE_SIZE,
    #                                   outline='black')
    #             tile.grid(column=x_iter, row=y_iter)

    def blue(self):
        self.color = 'blue'

    def green(self):
        self.color = 'green'

    def magenta(self):
        self.color = 'magneta'

    def disappear(self):
        """
        Remove Sammy's image from the Canvas
        Call appear to have the image reappear after a delay
        :return: None
        """
        self.canvas.delete(self.image_id)
        self.canvas.after(1000, self.appear)

    def appear(self):
        """
        Add Sammy's image to Canvas
        Call disappear to have the image disappear after a delay
        :return: None
        """
        self.image_id = self.canvas.create_image(150, 150,
                                                 image=self.sammy)
        self.canvas.after(1000, self.disappear)

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
    # check if the folder is in the directory
    if folder not in os.listdir():
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


if __name__ == '__main__':
    main()
