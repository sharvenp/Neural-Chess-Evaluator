from view import View
from controller import Controller
from chess_model import ChessModel
from engine import Engine

if __name__ == '__main__':
    m = ChessModel([('E', Engine(1, 1)), ('H', None)])
    c = Controller(m)
    v = View(c)
    m.add_observer(v)
    v.run()
