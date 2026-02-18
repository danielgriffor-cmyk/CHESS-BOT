import tkinter as tk
import chess
import random
import math

class Bot:
    def __init__(self, color=chess.BLACK, depth=2):
        self.color = color
        self.depth = depth

    def evaluate(self, board):
        """
        Override this method in subclasses.
        Should return a numeric evaluation from the perspective of self.color
        """
        raise NotImplementedError

    def all_moves(self, board):
        """
        Return a list of (move, is_nudge) that are safe for the current player.
        Uses an imaginary board for each move to check king safety.
        """
        moves = []

        turn_color = board.turn
        king_square = board.king(turn_color)

        # --- normal legal moves ---
        for move in board.legal_moves:
            temp_board = board.copy()
            temp_board.push(move)
            # check if our king is still safe
            if not temp_board.is_check():
                moves.append((move, False))

        return moves


    def minimax(self, board, depth=None, alpha=-1e9, beta=1e9, maximizing=None):
        if depth is None:
            depth = self.depth
        if maximizing is None:
            maximizing = board.turn == self.color

        if depth == 0 or board.is_game_over():
            return self.evaluate(board) + 0.01*random.random(), None

        best_move = None
        moves = self.all_moves(board)

        if maximizing:
            max_eval = -1e9
            for move, is_nudge in moves:
                board.push(move)
                eval_score, _ = self.minimax(board, depth-1, alpha, beta, False)
                board.pop()
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = (move, is_nudge)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval, best_move

        else:
            min_eval = 1e9
            for move, is_nudge in moves:
                board.push(move)
                eval_score, _ = self.minimax(board, depth-1, alpha, beta, True)
                board.pop()
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = (move, is_nudge)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def choose_move(self, board, depth=None):
        """
        Chooses the best move using minimax with alpha-beta pruning.
        Returns (move, is_nudge). Falls back to first legal move if none found.
        The score is automatically negated if the bot is black.
        """
        if depth is None:
            depth = self.depth

        # Maximizing if it's the bot's turn
        maximizing = board.turn == self.color

        score, best = self.minimax(board, depth, -1e9, 1e9, maximizing)

        if best is None:
            legal_moves = list(board.legal_moves)
            if legal_moves:
                return legal_moves[0], False
            return None, False

        return best
