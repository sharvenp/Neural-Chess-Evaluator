
from sklearn.neural_network import MLPRegressor
from matplotlib import pyplot as plt
from utils.util import Util
import numpy as np
import pickle
import time
import chess

class ChessEvaluator():
    
    def __init__(self, load_model=None):

        if load_model:
            self._model = pickle.load(open(load_model, "rb"))
        else:
            self._model = MLPRegressor((700, 500, 40),
                                        solver='sgd',
                                        learning_rate_init=0.001,
                                        shuffle=True,
                                        nesterovs_momentum=True,
                                        momentum=0.7,
                                        max_iter=200,
                                        batch_size=500,
                                        alpha=0.0005)
       
    def forward(self, board):
        return self._model.predict(Util.convert_to_bitmap_additional(board))

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

    model = ChessEvaluator(load_model="../models/vector-2.sav")

    board = chess.Board("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1")
    print(board)
    print(model.forward(board))