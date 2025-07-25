from config import COLUMN_COUNT
def is_board_full(board):
    return all(board[0][c] != '.' for c in range(COLUMN_COUNT))
