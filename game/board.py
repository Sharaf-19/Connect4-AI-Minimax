import numpy as np

class Board:
    ROW_COUNT = 6
    COLUMN_COUNT = 7

    def __init__(self):
        #Initializes an empty board
        self.board = np.zeros((self.ROW_COUNT, self.COLUMN_COUNT))

    def reset(self):
        self.board = np.zeros((self.ROW_COUNT, self.COLUMN_COUNT))

    def is_valid_location(self, col):
        #The topmost cell in a column is checked. If it equals 0, the column is not full.
        return self.board[self.ROW_COUNT - 1][col] == 0

    def get_next_open_row(self, col):
        #Finds the first available (empty) row in a given column.
        for r in range(self.ROW_COUNT):
            if self.board[r][col] == 0:
                return r

    def drop_piece(self, row, col, piece):
        self.board[row][col] = piece

    def winning_move(self, piece):
        # Check horizontal, vertical, and diagonal conditions
        for c in range(self.COLUMN_COUNT - 3):
            for r in range(self.ROW_COUNT):
                if all([self.board[r][c + i] == piece for i in range(4)]):
                    return True

        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT - 3):
                if all([self.board[r + i][c] == piece for i in range(4)]):
                    return True

        for c in range(self.COLUMN_COUNT - 3):
            for r in range(self.ROW_COUNT - 3):
                if all([self.board[r + i][c + i] == piece for i in range(4)]):
                    return True

            for r in range(3, self.ROW_COUNT):
                if all([self.board[r - i][c + i] == piece for i in range(4)]):
                    return True

        return False

    def get_valid_moves(self):
        #Returns a list of columns where moves are still valid
        return [col for col in range(self.COLUMN_COUNT) if self.is_valid_location(col)]
