from model_v1 import ChessEvaluator
from evaluation_functions.evaluation_function import EvaluationFunction


class Hugo(EvaluationFunction):

    def __init__(self):
        self.evaluator = ChessEvaluator("../models/hugo.sav")

    def evaluate(self, board):
        return self.evaluator.forward(board)
