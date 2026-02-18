import chess
import random
import ChessBotBase

class Bot(ChessBotBase.Bot):
    def evaluate(self, board):
        return 0