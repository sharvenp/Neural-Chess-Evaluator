import pygame as pg
from utils.settings import Settings
from utils.observer import Observer
from utils.util import Util


class View(Observer):

    def __init__(self, controller):
        self._controller = controller
        pg.init()
        pg.display.set_caption("Chess")
        self._screen = pg.display.set_mode((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))

    def update(self, o):

        square_width = (Settings.SCREEN_WIDTH - (Settings.BOARD_OFFSET * 2)) // 8

        # Draw squares
        alternator = False
        for i in range(8):
            for j in range(8):
                x = Settings.BOARD_OFFSET + square_width * j
                y = Settings.BOARD_OFFSET + square_width * i
                c = Settings.LIGHT_SQUARE_COLOR
                if alternator:
                    c = Settings.DARK_SQUARE_COLOR
                alternator = not alternator

                if j == 7:
                    alternator = not alternator

                pg.draw.rect(self._screen, c, (x, y, square_width, square_width))

        if o.get_from_square() is not None:
            # Draw selected square
            i = o.get_from_square()
            x, y = Util.convert_i_to_xy(i)
            pg.draw.rect(self._screen, Settings.SELECTED_SQUARE_COLOR, (x, y, square_width, square_width))

            # Draw legal moves
            for j in o.get_to_squares():
                x, y = Util.convert_i_to_xy(j)
                pg.draw.circle(self._screen, Settings.LEGAL_MARKER_COLOR, (x + square_width//2, y + square_width//2), 5)

        # Draw pieces
        board = o.get_board()
        for i in range(64):
            x, y = Util.convert_i_to_xy(i)

            p = board.piece_at(i)
            if p is None:
                continue

            c = ["b", "w"][int(p.color)]
            fn = f"{p.piece_type}{c}.png"
            piece_image = pg.image.load(f"resources/{fn}")
            piece_imagerect = piece_image.get_rect()
            piece_image = pg.transform.smoothscale(piece_image, (
                int(piece_imagerect.width * 1.3), int(piece_imagerect.height * 1.3)))
            piece_imagerect = piece_image.get_rect()
            piece_imagerect.center = (x + square_width / 2, y + square_width / 2)
            self._screen.blit(piece_image, piece_imagerect)

        pg.display.update()

    def run(self):

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return
                self._controller.handle(event)
