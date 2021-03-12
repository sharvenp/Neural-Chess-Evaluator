from utils.observable import Observable
import chess


class ChessModel(Observable):

    def __init__(self):
        Observable.__init__(self)
        self._turn = 0
        self._board = chess.Board("8/8/8/8/4k3/8/1q6/4K3 w - - 0 1")
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

    def make_engine_move(self, engine):
        print("Engine thinking...")
        move = engine.get_move(self._board)
        print("Engine playing move:", move)
        self._board.push(move)
        self._turn = (self._turn + 1) % 2
        self.notify_all()

    def get_board(self):
        return self._board

    def get_turn(self):
        return self._turn

    def get_from_square(self):
        return self._from_square

    def get_to_squares(self):
        return self._to_squares
