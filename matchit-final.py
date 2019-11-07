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
    num_clicks (int): number of click in one try
    num_of_tries(int): number of tries until the game done
    num_of_match (int): number of matched pairs
    score (int): score of the game
    color (string): the color chosen by player
    delay (int): the amount of time to flip the tiles
    folder (string): the folder holding the images
    pic (list): list of PhotoImage objects
    image_id (list): the image_ids associating with the clicked tiles
    click_tiles (list): list of id of the clicked tile_id
    new_list (list): list of 16 images in random order
    restart_btn (tkinter.Button): button to restart the game
    canvas (tkinter.Canvas): canvas to place 16 tiles
    score_label (tkinter.Label): label to displace the score/result
    """
    SQUARE_SIZE = 150
    NUM_GRIDS = 4
    CANVAS_SIZE = SQUARE_SIZE * NUM_GRIDS
    default_color = 'yellow'

    def __init__(self, parent, player_color, folder, delay):
        parent.title('Match it!')
        self.color = player_color
        self.delay = delay
        self.folder = folder
        # initialize data of the game
        self.reset_data()
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

    def reset_data(self):
        """
        Reset all the data of the game to the setup value
        :return: None
        """
        self.num_clicks = 0
        self.num_of_tries = 0
        self.num_of_match = 0
        self.score = 100
        self.pic = []
        self.image_id = []
        self.click_tiles = []  # list of the clicked tile_id
        self.new_list = self.shuffle_list()

    def restart(self):
        """
        This method is invoked when player clicks on the RESTART button.
        It shuffles and reassigns the images and resets the GUI and the
        score.
        :return: None
        """
        for tile in self.canvas.find_all():
            self.canvas.itemconfigure(tile, fill=self.default_color)
        self.reset_data()
        self.score_label.config(text=f'Score: {self.score}')


    def play(self, event):
        """
        This method is invoked when the user clicks on a tile.
        It implements the basic controls of the game.
        :param event: event (Event object) describing the click event
        :return: None
        """
        if self.num_clicks == 1:
            self.clickable(event)
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

    def clickable(self, event):
        """
        This is invoked when the user clicks on a tile if there less than 2
        tiles selected
        :param event: event (Event object) describing the click event
        :return: None
        """
        tile = self.canvas.find_closest(event.x, event.y)
        # check if tile is clickable, and already fill color
        if self.is_clickable(tile) and self.canvas.itemcget(tile, "fill") != \
                self.color:
            self.num_clicks += 1
            cords = self.canvas.coords(tile)
            self.canvas.itemconfigure(tile, tag="selected")
            self.pic.append(tkinter.PhotoImage(file=os.path.join(self.folder,
                                                                 self.new_list[
                                                                     tile[
                                                                         0] - 1])))
            self.image_id.append(self.canvas.create_image(
                (cords[0] + cords[2]) / 2,
                (cords[1] + cords[3]) / 2,
                image=self.pic[-1]))
            self.click_tiles.append(tile)

    def is_clickable(self, tile):
        """
        This method check if a tile is valid to be clicked
        :param tile: (tuple) the id of the tile
        :return: True if the tile can be clicked, false otherwise
        """
        return "match" not in self.canvas.gettags(tile) and \
               "selected" not in self.canvas.gettags(tile) and \
               len(self.canvas.find_withtag("selected")) < 2

    def check_match(self, click_tiles):
        """
        This method is used to check if 2 selected tiles are match
        :param click_tiles: (list) the list of 2 selected tiles
        :return: None
        """
        # is used when there are 2 tiles selected
        tile1 = click_tiles[0]
        tile2 = click_tiles[1]
        if self.new_list[tile1[0] - 1] == self.new_list[tile2[0] - 1]:
            # Add match and selected tag
            self.num_of_match += 1
            print(f'Num of match {self.num_of_match}')
            self.canvas.itemconfigure(tile1, tag=("match", "selected"))
            self.canvas.itemconfigure(tile2, tag=("match", "selected"))

    def flip_back(self):
        """
        This method is used to flip the 2 selected tiles after a delay
        :return: None
        """
        for img in self.image_id:
            self.canvas.delete(img)
        self.image_id.clear()
        for tile in self.canvas.find_withtag("match"):
            self.canvas.itemconfigure(tile, fill=self.color)
            # If item has match tag, removes all the tags
            self.canvas.itemconfigure(tile, tag="")
        for tile in self.canvas.find_withtag("selected"):
            self.canvas.itemconfigure(tile, fill=self.default_color)
            self.canvas.itemconfigure(tile, tag="")
        # check if all tiles are matched, update result label
        if self.num_of_match == 8:
            text_label = f'Game Over!\n Score: {self.score}\n ' \
                         f'Number of tries: {self.num_of_tries}'
            self.score_label.config(text=text_label)

    def create_grid(self):
        """
        This method is used to draw 16 tiles on canvas
        :return: None
        """
        for y_iter in range(self.NUM_GRIDS):
            for x_iter in range(self.NUM_GRIDS):
                x, y = x_iter * self.SQUARE_SIZE, y_iter * self.SQUARE_SIZE
                x_stop, y_stop = x + self.SQUARE_SIZE, y + self.SQUARE_SIZE
                cords = x, y, x_stop, y_stop
                self.canvas.create_rectangle(cords, outline=self.color,
                                             fill=self.default_color)

    def shuffle_list(self):
        """
        Create the full list of image files
        :return: (list) list of image files in random order
        """
        eight_pic = get_image_list(self.folder)
        if len(eight_pic) > 8:
            random.shuffle(eight_pic)
        full_list = eight_pic[:9] * 2
        random.shuffle(full_list)
        return full_list


def get_arguments():
    """
    Parse and validate the command line arguments
    :return: tuple containing color (string), image_folder(string),
        fast(int)
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
    :param folder: (string) the path of the folder containing gif files
    :return: (string) the valid folder
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
    """
    Extract the gif files in the given folder
    :param folder: (string) folder containing the gif files
    :return: (list): list of gif files in the folder
    """
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
