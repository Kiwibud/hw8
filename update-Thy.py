# create Tile object
# add Tiles to the canvas
    def create_grid(self):
        for y_iter in range(self.NUM_GRIDS):
            for x_iter in range(self.NUM_GRIDS):
                x, y = x_iter * self.SQUARE_SIZE, y_iter * self.SQUARE_SIZE
                x_stop, y_stop = x + self.SQUARE_SIZE, y + self.SQUARE_SIZE
                cords = x,y,x_stop, y_stop
                tile_id = x_iter*y_iter + x_iter
                image_file = os.path.join(self.folder, self.new_list[tile_id])
                tile = Tile(self.canvas, tile_id, image_file, cords,
                            self.player_color)


    def select(self, event):
        tile = self.canvas.find_withtag(tkinter.CURRENT)
        # self.canvas.itemconfigure(tile, tag="selected")
        if "selected" in self.canvas.gettags(tile):
            self.canvas.itemconfigure(tile, tag="")
        else:
            self.canvas.itemconfigure(tile, tag="selected")

class Tile:
    SQUARE_SIZE = 150
    default_color = 'yellow'

    def __init__(self, parent, tile_id, image_dir, cords, color):
        self.parent = parent
        self.tile_id = tile_id
        self.image_file = image_dir
        self.flipped = False
        self.color = color
        self.cords = cords
        self.visual = self.parent.create_rectangle(cords, outline=self.color, 
                                                   fill=self.default_color)

    def set_color(self, color):
        self.visual(fill=color)

    def flip(self):
        if not self.flipped:
            self.flipped = True
        else:
            self.flipped = False
