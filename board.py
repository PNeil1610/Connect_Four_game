from config import ROW_COUNT, COLUMN_COUNT

def create_board():
    return [['.' for _ in range(COLUMN_COUNT)] for _ in range(ROW_COUNT)]

def drop_disc(board, col, player):
    if col < 0 or col >= COLUMN_COUNT:
        return False
    for row in range(ROW_COUNT - 1, -1, -1):
        if board[row][col] == '.':
            board[row][col] = player
            return True
    return False

def check_win(board, player):
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            if all(board[r][c + i] == player for i in range(4)):
                return True
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if all(board[r + i][c] == player for i in range(4)):
                return True
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            if all(board[r + i][c + i] == player for i in range(4)):
                return True
    for r in range(ROW_COUNT - 3):
        for c in range(3, COLUMN_COUNT):
            if all(board[r + i][c - i] == player for i in range(4)):
                return True
    return False

