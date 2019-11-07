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
    CANVAS_SIZE = SQUARE_SIZE * NUM_GRIDS
    score = 100
    num_of_tries = 0
    default_color = 'yellow'
    num_of_match = 0

    def __init__(self, parent, player_color, folder, delay):
        self.num_clicks = 0
        parent.title('Match it!')
        self.color = player_color
        self.delay = delay
        self.folder = folder
        self.pic = []
        self.image_id = []
        # self.tiles = []  # array of all the Tile objects
        self.click_tiles = []  # array of all the clicked tile_id
        # Initiate list of images
        eight_pic = get_image_list(folder)
        if len(eight_pic) > 8:
            eight_pic = random.shuffle(get_image_list(folder))[:9]
        self.new_list = eight_pic*2
        random.shuffle(self.new_list)
        # Initialize self.sammy
        # self.pic = tkinter.PhotoImage(file=os.path.join(self.folder,
        #                                               self.new_list[0]))
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
        self.canvas.bind("<Button-1>", self.play)
        # Create a label widget for the score and end of game messages
        self.score_label = tkinter.Label(parent, text=f'Score: {self.score}',
                                         borderwidth=1)
        self.score_label.grid()
        # Create any additional instance variable you need for the game

    def text_label(self):
        if len(self.canvas.find_withtag("match")) == 16:
            return f'Game Over\n Score: {self.score}\n ' \
                   f'Num of tries: {self.num_of_tries}'

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
        # self.num_clicks += 1
        if self.num_clicks == 1:
            self.clickable(event)
            # if there is 2 tile with selected tag then we do following stuff
            if len(self.canvas.find_withtag("selected")) == 2:
                self.num_of_tries += 1
                print(f'Number of tries {self.num_of_tries}')
                if self.num_of_tries > 13:
                    self.score -= 10
                    self.score_label.config(text=f'Score: {self.score}')
                self.check_match(self.click_tiles)
                self.canvas.after(self.delay, self.flip_back)
                self.click_tiles.clear()
                self.num_clicks = 0
        else:
            self.clickable(event)

        if self.num_of_match == 8:
            text_label = f'Game Over!\n Score: {self.score}\n ' \
                         f'Number of tries: {self.num_of_tries}'
            self.score_label.config(text=text_label)

    def clickable(self, event):
        # this is when less then 2 tiles are selected
        tile = self.canvas.find_closest(event.x, event.y)
        # tile fill color = self.color, then it is not clickable so this fail
        if self.is_clickable(tile) and self.canvas.itemcget(tile, "fill") != \
                self.color:
            self.num_clicks += 1
            cords = self.canvas.coords(tile)
            self.canvas.itemconfigure(tile, tag="selected")
            self.pic.append(tkinter.PhotoImage(file=os.path.join(self.folder,
                                               self.new_list[tile[0]-1])))
            self.image_id.append(self.canvas.create_image(
                                (cords[0] + cords[2]) / 2,
                                 (cords[1] + cords[3]) / 2,
                                 image=self.pic[-1]))
            self.click_tiles.append(tile)

    def is_clickable(self, tile):
        return "match" not in self.canvas.gettags(tile) and \
               "selected" not in self.canvas.gettags(tile) and \
               len(self.canvas.find_withtag("selected")) < 2

    def check_match(self, click_tiles):
        # is used when there are 2 tiles selected
        tile1 = click_tiles[0]
        tile2 = click_tiles[1]
        if self.new_list[tile1[0]-1] == self.new_list[tile2[0]-1]:
            # Add match and selected tag
            self.num_of_match += 1
            self.canvas.itemconfigure(tile1, tag=("match", "selected"))
            self.canvas.itemconfigure(tile2, tag=("match", "selected"))

    def flip_back(self):
        for img in self.image_id:
            self.canvas.delete(img)
        self.image_id.clear()
        for tile in self.canvas.find_withtag("match"):
            self.canvas.itemconfigure(tile, fill=self.color)
            # If item has match tag, removes all the tag
            self.canvas.itemconfigure(tile, tag="")
        for tile in self.canvas.find_withtag("selected"):
            self.canvas.itemconfigure(tile, fill=self.default_color)
            self.canvas.itemconfigure(tile, tag="")

    def create_grid(self):
        for y_iter in range(self.NUM_GRIDS):
            for x_iter in range(self.NUM_GRIDS):
                x, y = x_iter * self.SQUARE_SIZE, y_iter * self.SQUARE_SIZE
                x_stop, y_stop = x + self.SQUARE_SIZE, y + self.SQUARE_SIZE
                cords = x, y, x_stop, y_stop
                self.canvas.create_rectangle(cords, outline=self.color,
                                             fill=self.default_color)

    def select(self, event):
        tile = self.canvas.find_withtag(tkinter.CURRENT)
        print(tile)
        if "selected" in self.canvas.gettags(tile):
            self.canvas.itemconfigure(tile, tag="")
        else:
            self.canvas.itemconfigure(tile, tag="selected")
        return tile


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
    if not os.path.exists(folder):
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
