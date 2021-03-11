from utils.observable import Observable
import chess


class ChessModel(Observable):

    def __init__(self):
        Observable.__init__(self)
        self._board = chess.Board()

    def get_board(self):
        return self._board