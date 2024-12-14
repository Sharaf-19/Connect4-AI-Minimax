import math
import random

class Minimax:
    #limits the depth of the Minimax recursion, 
    MAX_DEPTH = 5

    def __init__(self, board):
        self.board = board

    def minimax(self, depth, alpha, beta, maximizing_player):
        valid_moves = self.board.get_valid_moves()
        is_terminal = self.board.winning_move(1) or self.board.winning_move(2) or len(valid_moves) == 0

        if depth == 0 or is_terminal:
            if is_terminal:
                if self.board.winning_move(2):
                    # returns favorable outcome if AI wins
                    return None, math.inf 
                elif self.board.winning_move(1):
                    # returns unfavorable outcome if Human wins, & AI loses
                    return None, -math.inf 
                else:
                    return None, 0 # returns 0 if draw
            else:
                #If the depth is 0, recursion ends, and board evaluated using heuristic evaluate_board()
                return None, self.evaluate_board()

        if maximizing_player:
            # AI seeks to maximize the score, value will be -inf
            value = -math.inf 
            column = random.choice(valid_moves)
            for col in valid_moves:
                row = self.board.get_next_open_row(col)
                temp_board = self.board.board.copy() #Save a copy of the current board state.
                self.board.drop_piece(row, col, 2)
                _, new_score = self.minimax(depth - 1, alpha, beta, False)
                self.board.board = temp_board
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value

        else:
            # opponent seeks to minimize the score, then 'value = infinity'
            value = math.inf
            column = random.choice(valid_moves)
            for col in valid_moves:
                row = self.board.get_next_open_row(col)
                temp_board = self.board.board.copy() 
                self.board.drop_piece(row, col, 1)
                _, new_score = self.minimax(depth - 1, alpha, beta, True)
                self.board.board = temp_board
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value
    
    #Computes a heuristic score to evaluate how favorable the board state is for the AI
    def evaluate_board(self):
      score = 0

      # Scoring for center column
      center_array = [self.board.board[r][self.board.COLUMN_COUNT // 2] for r in range(self.board.ROW_COUNT)]
      center_count = center_array.count(2)
      score += center_count * 3

      # Horizontal scoring
      for r in range(self.board.ROW_COUNT):
          row_array = [self.board.board[r][c] for c in range(self.board.COLUMN_COUNT)]
          for c in range(self.board.COLUMN_COUNT - 3):
              window = row_array[c:c + 4]
              score += self.score_window(window)

      # Vertical scoring
      for c in range(self.board.COLUMN_COUNT):
          col_array = [self.board.board[r][c] for r in range(self.board.ROW_COUNT)]
          for r in range(self.board.ROW_COUNT - 3):
              window = col_array[r:r + 4]
              score += self.score_window(window)

      # Positive diagonal scoring
      for r in range(self.board.ROW_COUNT - 3):
          for c in range(self.board.COLUMN_COUNT - 3):
              window = [self.board.board[r + i][c + i] for i in range(4)]
              score += self.score_window(window)

      # Negative diagonal scoring
      for r in range(3, self.board.ROW_COUNT):
          for c in range(self.board.COLUMN_COUNT - 3):
              window = [self.board.board[r - i][c + i] for i in range(4)]
              score += self.score_window(window)

      return score

    def score_window(self, window):
        score = 0
        ai_piece = 2
        player_piece = 1
        empty = 0

        if window.count(ai_piece) == 4:
            score += 100
        elif window.count(ai_piece) == 3 and window.count(empty) == 1:
            score += 5
        elif window.count(ai_piece) == 2 and window.count(empty) == 2:
            score += 2

        if window.count(player_piece) == 4:
            score -= 100
        elif window.count(player_piece) == 3 and window.count(empty) == 1:
            score -= 4
        elif window.count(player_piece) == 2 and window.count(empty) == 2:
            score -= 1

        return score

