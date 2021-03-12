import chess
import concurrent.futures

class Engine:

    def __init__(self, side, depth_limit, evaluation_function):
        self._side = side
        self._evaluation_function = evaluation_function
        self._depth_limit = depth_limit

    def get_move(self, curr_state):

        best_move = None
        best_eval = 10000
        features = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            for move in curr_state.legal_moves:
                copy = curr_state.copy()
                copy.push(move)
                if copy.is_game_over():
                    print("Game over state")
                f = executor.submit(self._minmax, copy, self._depth_limit, False, -10000, 10000)
                features.append((f, move))

        for [f, move] in features:
            evaluation = f.result()
            if evaluation < best_eval:
                best_eval = evaluation
                best_move = move

        print(f"Best move: {best_move} ({best_eval})")

        return best_move

    def _minmax(self, state, depth, maximizing_player, alpha, beta):

        result = self._is_game_over(state)
        if result is not None:
            # Game over
            return result

        if depth == 0:
            return self._evaluation_function.evaluate(state)

        # Game continues
        if maximizing_player:
            # Maximize engine
            value = -10000
            for move in state.legal_moves:
                state.push(move)
                value = max(value, self._minmax(state, depth - 1, not maximizing_player, alpha, beta))
                state.pop()
                # beta = min(beta, value)
                # if beta <= alpha:
                #     break
            return value
        else:
            # Minimize opponent
            value = 10000
            for move in state.legal_moves:
                state.push(move)
                value = min(value, self._minmax(state, depth - 1, not maximizing_player, alpha, beta))
                state.pop()
                # alpha = max(alpha, value)
                # if beta <= alpha:
                #     break
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
