
from chess_model import ChessModel
import pygame as pg

class Controller:

    def __init__(self, chess_model):
        self._chess_model = chess_model
        self._is_dragging_mouse = False

    def handle(self, event):

        if event.type == pg.MOUSEBUTTONDOWN:
            self._is_dragging_mouse = True
            mx, my = pg.mouse.get_pos()

        if event.type == pg.MOUSEBUTTONUP:
            self._is_dragging_mouse = False
