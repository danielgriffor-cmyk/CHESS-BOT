import tkinter as tk
import chess
import chess.pgn
import SimpleChessBot
import HumanChessBot

SQUARE_SIZE = 70
LIGHT = "#f0d9b5"
DARK = "#b58863"
HIGHLIGHT = "#88ff88"
NUDGE_HIGHLIGHT = "#88aaff"

BOT_COLOR = chess.BLACK

UNICODE_PIECES = {
    "P": "♙", "N": "♘", "B": "♗", "R": "♖", "Q": "♕", "K": "♔",
    "p": "♟", "n": "♞", "b": "♝", "r": "♜", "q": "♛", "k": "♚",
}

# ---------------- GUI ---------------- #

class chessGUI:
    def __init__(self, white_player='human', black_player=None):
        self.move_time = 100
        self.board = chess.Board()
        self.white_player = white_player
        self.black_player = black_player

        self.root = tk.Tk()
        self.root.title("Chess")

        self.canvas = tk.Canvas(
            self.root,
            width=8*SQUARE_SIZE,
            height=8*SQUARE_SIZE
        )
        self.canvas.pack()

        # 🔑 Make sure images exist before draw()
        self.images = {}
        self.load_images()

        self.selected = None
        self.legal_targets = []
        self.nudge_targets = []

        self.status = tk.Label(self.root, text="", font=("Arial", 14))
        self.status.pack()

        self.canvas.bind("<Button-1>", self.on_click)
        self.draw()

        # Start bot move immediately if it's bot vs bot and Black is first
        self.root.after(self.move_time, self.bot_turn)

    def load_images(self):
        piece_map = {
            "P": "w_pawn",
            "N": "w_knight",
            "B": "w_bishop",
            "R": "w_rook",
            "Q": "w_queen",
            "K": "w_king",
            "p": "b_pawn",
            "n": "b_knight",
            "b": "b_bishop",
            "r": "b_rook",
            "q": "b_queen",
            "k": "b_king",
        }

        for symbol, name in piece_map.items():
            img = tk.PhotoImage(file=f"pieces/{name}.png")
            img = img.subsample(2, 2)  # resize as needed
            self.images[symbol] = img

    # ----------------- Keep all other methods from your previous GUI -----------------
    # draw(), on_click(), compute_targets(), bot_turn(), after_player_move(), update_status(), etc.


    # ---------------- Existing methods ----------------
    # load_images(), update_status(), square_at(), draw(),
    # compute_targets(), etc. remain the same

    def draw(self):
        self.canvas.delete("all")
        for r in range(8):
            for f in range(8):
                x1 = f * SQUARE_SIZE
                y1 = (7 - r) * SQUARE_SIZE
                color = LIGHT if (r + f) % 2 == 0 else DARK
                sq = chess.square(f, r)

                if sq in self.legal_targets:
                    color = HIGHLIGHT
                if sq in self.nudge_targets:
                    color = NUDGE_HIGHLIGHT

                self.canvas.create_rectangle(
                    x1, y1, x1 + SQUARE_SIZE, y1 + SQUARE_SIZE, fill=color
                )

                piece = self.board.piece_at(sq)
                if piece:
                    self.canvas.create_image(
                        x1 + SQUARE_SIZE // 2,
                        y1 + SQUARE_SIZE // 2,
                        image=self.images[piece.symbol()]
                    )

    def square_at(self, x, y):
        file = x // SQUARE_SIZE
        rank = 7 - (y // SQUARE_SIZE)
        return chess.square(file, rank)


    def compute_targets(self, square):
        self.legal_targets.clear()
        self.nudge_targets.clear()

        # normal legal moves
        for m in self.board.legal_moves:
            if m.from_square == square:
                self.legal_targets.append(m.to_square)

    def update_status(self):
        if self.board.is_checkmate():
            winner = "Black" if self.board.turn == chess.WHITE else "White"
            self.status.config(text=f"Checkmate! {winner} wins.")
            return True

        if self.board.is_stalemate():
            self.status.config(text="Stalemate! Draw.")
            return True

        if self.board.is_check():
            side = "White" if self.board.turn == chess.WHITE else "Black"
            self.status.config(text=f"{side} is in check!")
        else:
            self.status.config(text="")

        return False

    # ---------------- Updated click logic ----------------
    def on_click(self, event):
        if self.board.is_game_over():
            return

        current_player = self.white_player if self.board.turn == chess.WHITE else self.black_player
        if current_player != 'human':
            return  # ignore clicks if bot's turn

        sq = self.square_at(event.x, event.y)

        if self.selected is None:
            piece = self.board.piece_at(sq)
            if piece and piece.color == self.board.turn:
                self.selected = sq
                self.compute_targets(sq)
        else:
            if sq in self.legal_targets or sq in self.nudge_targets:
                self.board.push(chess.Move(self.selected, sq))
                self.after_player_move()

            self.selected = None
            self.legal_targets.clear()
            self.nudge_targets.clear()

        self.draw()

    # ---------------- Updated bot logic ----------------
    def bot_turn(self):
        if self.board.is_game_over():
            return

        current_player = self.white_player if self.board.turn == chess.WHITE else self.black_player
        if current_player == 'human' or current_player is None:
            return  # skip if human turn

        # get move from the bot
        move, is_nudge = current_player.choose_move(self.board)

        if move is not None:
            self.board.push(move)
            self.draw()
            self.update_status()

        # if bot vs bot, schedule next bot move
        next_player = self.white_player if self.board.turn == chess.WHITE else self.black_player
        if next_player != 'human' and not self.board.is_game_over():
            self.root.after(self.move_time, self.bot_turn)

    def after_player_move(self):
        if self.update_status():
            return
        self.root.after(self.move_time, self.bot_turn)

    # ---------------- Existing run method ----------------
    def run(self):
        self.root.mainloop()

white_bot = HumanChessBot.Bot(chess.BLACK, depth=2)
black_bot = SimpleChessBot.Bot(chess.BLACK, depth=2)

gui = chessGUI(white_player=white_bot, black_player=black_bot)
gui.move_time = 100
gui.run()

print(chess.pgn.Game.from_board(gui.board))