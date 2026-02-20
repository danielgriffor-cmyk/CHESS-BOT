import tkinter as tk
import chess
import chess.pgn
from ChessGUI import chessGUI

import SimpleChessBot
import ComplexChessBot
import RandomChessBot
import CheckChessBot

white_bot = ComplexChessBot.Bot(color = chess.WHITE, depth=2)
black_bot = ComplexChessBot.Bot(color = chess.BLACK, depth=3, qsearch=False)

gui = chessGUI(white_player=white_bot, black_player=black_bot)
gui.move_time = 1

gui.run()

print(chess.pgn.Game.from_board(gui.board))
