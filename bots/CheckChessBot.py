import chess
import random
import base.ChessBotBase as ChessBotBase
import math

class Bot(ChessBotBase.Bot):
    def evaluate(self, board):
        score = 0
        
        if board.is_checkmate():
            return -1e6 if board.turn == self.color else 1e6
        
        if board.is_check():
            score += 1500 if board.turn == self.color else 1500
        
        return score

