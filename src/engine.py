
from model_v1 import ChessEvaluator
import chess
import random

class Engine:

    def __init__(self, side, depth_limit):
        self._side = side
        self._evaluator = ChessEvaluator(load_model="../models/hugo.sav")
        self._depth_limit = depth_limit

    def get_move(self, curr_state):

        best_move = None
        best_eval = -1000
        for move in curr_state.legal_moves:
            curr_state.push(move)
            evaluation = self._minmax(curr_state, 0, True, -1000, 1000)
            if evaluation > best_eval:
                best_eval = evaluation
                best_move = move
            curr_state.pop()

        return best_move

    def _minmax(self, state, depth, isMaximizingPlayer, alpha, beta):

        result = self._is_game_over(state)
        if result is not None:
            # Game over
            return result

        if depth == self._depth_limit:
            return abs(self._evaluator.forward(state))

        # Game continues
        if isMaximizingPlayer:
            # Maximize engine
            value = -1000
            for move in state.legal_moves:
                state.push(move)
                value = max(value, self._minmax(state, depth + 1, False, alpha, beta))
                state.pop()
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
            return value
        
        else:
            # Minimize opponent
            value = 1000
            for move in state.legal_moves:
                state.push(move)
                value = min(value, self._minmax(state, depth + 1, False, alpha, beta))
                state.pop()
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return value

    def _is_game_over(self, state):
        result_dict = {
            "1-0": 10000,
            "0-1": -10000,
            "1/2-1/2": 0,
            "*": None        
        }

        return result_dict[state.result()]

if __name__ == '__main__':
    e = Engine(1, 3)
    b = chess.Board()
    print(e.get_move(b))