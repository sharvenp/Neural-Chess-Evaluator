from view import View
from controller import Controller
from chess_model import ChessModel
from engine import Engine
from evaluation_functions.hugo import Hugo

if __name__ == '__main__':
    m = ChessModel()
    c = Controller(m)
    v = View(c, [('H', None), ('E', Engine(1, 3, Hugo()))])
    m.add_observer(v)
    v.run()
