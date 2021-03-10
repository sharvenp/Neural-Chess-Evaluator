
from sklearn.neural_network import MLPRegressor
from matplotlib import pyplot as plt
import numpy as np
import pickle
import time
import chess

class ChessEvaluator():
    
    def __init__(self, load_model=None):

        if load_model:
            self._model = pickle.load(open(load_model, "rb"))
        else:
            self._model = MLPRegressor((500, 300, 20),
                                        solver='sgd',
                                        learning_rate_init=0.001,
                                        shuffle=True,
                                        nesterovs_momentum=True,
                                        momentum=0.7,
                                        max_iter=200,
                                        batch_size=500,
                                        alpha=0.00018)
        
    def _convert_board_to_bitmap(self, board):

        bitmap = []

        piece_id = [1, 2, 3, 4, 5, 6]
        color_id = [True, False]

        for color in color_id:
            for piece in piece_id:
                for i in range(64):
                    p = board.piece_at(i)
                    
                    if p is None:
                        bitmap.append(0)
                        continue

                    if p.piece_type == piece and p.color == color:
                        bitmap.append(1)
                    else:
                        bitmap.append(0)

        for color in color_id:
            bitmap.append(int(board.has_kingside_castling_rights(color)))
            bitmap.append(int(board.has_queenside_castling_rights(color)))

        return np.array(bitmap).reshape(1, -1)

    def forward(self, board):
        return self._model.predict(self._convert_board_to_bitmap(board))

    def train(self, train_X, train_Y, val_X, val_Y, num_epochs=5):
        print("Training model...")
      
        train_scores = []
        val_scores = []

        for i in range(num_epochs):
            shuffler = np.random.permutation(len(train_X))
            train_X = train_X[shuffler]
            train_Y = train_Y[shuffler]
            start_time = time.time()
            self._model.partial_fit(train_X, train_Y)
            train_score = self._model.score(train_X, train_Y)
            val_score = self._model.score(val_X, val_Y)
            print(f"Epoch: {i} -- Train Score: {train_score} -- Validation Score: {val_score} -- T: {time.time() - start_time}s")
            train_scores.append(train_score)
            val_scores.append(val_score)

        plt.plot(range(num_epochs), train_scores)
        plt.plot(range(num_epochs), val_scores)
        plt.show()

        print("Model Trained.")
        pickle.dump(self._model, open(f"vector.sav", 'wb'))
        print("Saved model.")

    def test(self, test_X, test_y):
        score = self._model.score(test_X, test_y)
        return score

if __name__ == "__main__":

    model = ChessEvaluator(load_model="../models/vector.sav")

    board = chess.Board("r1bqkbnr/1ppp1Qpp/p1n5/4p3/4P3/3B4/PPPP1PPP/RNB1K1NR b KQkq - 0 1")
    print(board)
    print(model.forward(board))