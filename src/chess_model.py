from utils.observable import Observable
import chess
from engine import Engine

class ChessModel(Observable):

    def __init__(self, players):
        Observable.__init__(self)
        self._players = players
        self._turn = 0
        self._board = chess.Board()
        self._from_square = None
        self._to_squares = []

    def select_from_square(self, i):
        if self._board.piece_at(i) is None:
            return

        self._from_square = i
        self._to_squares = []

        for j in range(64):
            if i == j:
                continue
            try:
                _ = self._board.find_move(i, j)
                self._to_squares.append(j)
            except ValueError:
                pass

        self.notify_all()

    def select_to_square(self, i):
        if i in self._to_squares:
            move = self._board.find_move(self._from_square, i)
            self._board.push(move)
            self._turn = (self._turn + 1) % 2

        self._from_square = None
        self._to_squares = []
        self.notify_all()

        if self._board.is_game_over():
            print("Game Over:", self._board.result())
            return

        if self._players[self._turn][0] == "E":
            self._make_engine_move()

    def make_engine_move(self):
        print("Engine thinking...")
        move = self._players[self._turn][1].get_move(self._board)
        print("Engine playing move:", move)
        self._board.push(move)
        self._turn = (self._turn + 1) % 2
        self.notify_all()

    def get_board(self):
        return self._board

    def get_from_square(self):
        return self._from_square

    def get_to_squares(self):
        return self._to_squares
