import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import math

from game import Board
from game import Minimax

class Connect4GUI:
    SQUARESIZE = 120
    MY_COLOR = "white"
    AI_COLOR = "#ffb301" #yellow
    EMPTY_COLOR = "gray"

    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Connect 4")
        self.root.geometry("740x780")

        self.board = Board()
        self.minimax = Minimax(self.board)
        self.turn = 0
        self.game_over = False
        self.player_score = 0
        self.ai_score = 0

        self.setup_ui()

    def setup_ui(self):
        frame = ctk.CTkFrame(self.root)
        frame.pack(pady=10)

        self.name = ctk.CTkLabel(frame, text='Player Name: ')
        self.name.grid(row=0, column=0, padx=5)

        self.player_name_entry = ctk.CTkEntry(frame)
        self.player_name_entry.grid(row=0, column=1, padx=5)
        
        start_button = ctk.CTkButton(frame, text="Start", fg_color="green", hover_color='gray', command=self.start_game)
        start_button.grid(row=0, column=2, padx=5)

        reset_button = ctk.CTkButton(frame, text="Reset", fg_color="red", hover_color='gray', command=self.reset_board)
        reset_button.grid(row=0, column=3, padx=5)

        self.canvas = ctk.CTkCanvas(self.root, width=self.board.COLUMN_COUNT * self.SQUARESIZE, height=self.board.ROW_COUNT * self.SQUARESIZE, bg="#576486")
        self.canvas.pack(pady=10)
        self.canvas.bind("<Button-1>", self.handle_click)

        self.winner_label = ctk.CTkLabel(self.root, text="", font=("fixedsys", 30))
        self.winner_label.pack(pady=5)

        self.scoreboard_label = ctk.CTkLabel(self.root, text="Scoreboard", font=("fixedsys", 30))
        self.scoreboard_label.pack(pady=5)

    def start_game(self):
        self.reset_board()
        CTkMessagebox(title="Connect 4", 
                  message= f"Game Started!! \nGood luck {self.player_name_entry.get()}!")
        self.winner_label.configure(text=f"{self.player_name_entry.get() or 'Player'}'s turn...", text_color='white')
        
    def reset_board(self):
        self.board.reset()
        self.turn = 0
        self.game_over = False
        self.update_board()
        self.winner_label.configure(text="")
        self.update_scoreboard()

    def update_board(self):
        self.canvas.delete("all")
        for r in range(self.board.ROW_COUNT):
            for c in range(self.board.COLUMN_COUNT):
                color = self.EMPTY_COLOR
                if self.board.board[r][c] == 1:
                    color = self.MY_COLOR
                elif self.board.board[r][c] == 2:
                    color = self.AI_COLOR

                visual_row = self.board.ROW_COUNT - r - 1
                self.canvas.create_oval(
                    c * self.SQUARESIZE + 10,
                    visual_row * self.SQUARESIZE + 10,
                    (c + 1) * self.SQUARESIZE - 10,
                    (visual_row + 1) * self.SQUARESIZE - 10,
                    fill=color,
                    outline=color
                )

    def update_scoreboard(self):
        player_name = self.player_name_entry.get() or "Player"
        self.scoreboard_label.configure(text=f"{player_name}: {self.player_score} | AI: {self.ai_score}")

    def handle_click(self, event):
        if self.game_over:
            return

        x = event.x
        col = x // self.SQUARESIZE

        if self.board.is_valid_location(col):
            row = self.board.get_next_open_row(col)
            if self.turn % 2 == 0:
                self.board.drop_piece(row, col, 1)
                self.update_board()
                if self.board.winning_move(1):
                    self.game_over = True
                    self.player_score += 1
                    self.winner_label.configure(text=f"{self.player_name_entry.get() or 'Player'} is the winner 🏆", fg_color="green")
                else:
                    self.turn += 1
                    self.winner_label.configure(text="AI's turn...", text_color="#ffb301")
                    self.root.after(1200, self.ai_turn)

    def ai_turn(self):
        if not self.game_over:
            col, _ = self.minimax.minimax(Minimax.MAX_DEPTH, -math.inf, math.inf, True)
            
            if self.board.is_valid_location(col):
                row = self.board.get_next_open_row(col)
                self.board.drop_piece(row, col, 2)
                self.update_board()
                if self.board.winning_move(2):
                    self.game_over = True
                    self.ai_score += 1
                    self.winner_label.configure(text="AI is the winner 🏆", fg_color="green")
                else:
                    self.turn += 1
                    self.winner_label.configure(text=f"{self.player_name_entry.get() or 'palyer'}'s turn..", text_color="white")

    def run(self):
        self.root.mainloop()
