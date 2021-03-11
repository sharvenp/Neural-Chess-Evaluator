from view import View
from controller import Controller
from chess_model import ChessModel

if __name__ == '__main__':
    m = ChessModel()
    c = Controller(m)
    v = View(c)
    m.add_observer(v)
    m.notify_all()
    v.run()
