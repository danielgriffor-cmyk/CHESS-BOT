import tkinter as tk
import chess
import chess.pgn
from ChessGUI import chessGUI

import SimpleChessBot
import ComplexChessBot
import RandomChessBot
import CheckChessBot

white_bot = ComplexChessBot.Bot(chess.WHITE, depth=3)
black_bot = ComplexChessBot.Bot(chess.BLACK, depth=3)

gui = chessGUI(white_player=white_bot, black_player=black_bot)
gui.move_time = 100
gui.run()

print(chess.pgn.Game.from_board(gui.board))
