import pygame as pg
from utils.settings import Settings
from utils.observer import Observer


class View(Observer):

    def __init__(self, controller):
        self._controller = controller
        pg.init()
        pg.display.set_caption("Chess")
        self._screen = pg.display.set_mode((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))

    def update(self, o):

        square_width = (Settings.SCREEN_WIDTH - (Settings.BOARD_OFFSET*2)) // 8

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

        board = o.get_board()
        for i in range(64):

            row = i // 8
            col = i % 8
            x = Settings.BOARD_OFFSET + square_width * col
            y = Settings.BOARD_OFFSET + square_width * row

            p = board.piece_at(i)
            if p is None:
                continue

            c = ["b", "w"][int(p.color)]
            fn = f"{p.piece_type}{c}.png"
            piece_image = pg.image.load(f"resources/{fn}")
            piece_imagerect = piece_image.get_rect()
            piece_image = pg.transform.smoothscale(piece_image, (int(piece_imagerect.width * 1.3), int(piece_imagerect.height * 1.3)))
            piece_imagerect = piece_image.get_rect()
            piece_imagerect.center = (x + square_width/2, y + square_width/2)
            self._screen.blit(piece_image, piece_imagerect)

        pg.display.update()

    def run(self):

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return

                self._controller.handle(event)
