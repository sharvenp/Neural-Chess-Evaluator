
from chess_model import ChessModel
from utils.settings import Settings
from utils.util import Util

import pygame as pg

class Controller:

    def __init__(self, chess_model):
        self._chess_model = chess_model

    def handle(self, event):

        if event.type == pg.MOUSEBUTTONDOWN:
            mx, my = pg.mouse.get_pos()
            r, c = Util.convert_xy_to_rc(mx, my)
            i = Util.convert_rc_to_i(r, c)

            if self._chess_model._from_square is None:
                self._chess_model.select_from_square(i)
            else:
                self._chess_model.select_to_square(i)
