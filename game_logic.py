from config import ROW_COUNT, COLUMN_COUNT, SQUARESIZE
from graphics import draw_reset_button

def handle_input(x, y, screen, board, current_player, game_over, dropping):
    button_rect = draw_reset_button(screen)
    if button_rect.collidepoint(x, y):
        return "reset"
    if not game_over and not dropping and SQUARESIZE <= y < (ROW_COUNT + 1) * SQUARESIZE: #click in the board area to drop a disc
        col_clicked = x // SQUARESIZE
        for r in range(ROW_COUNT - 1, -1, -1):
            if board[r][col_clicked] == '.':
                return (r, col_clicked)
    return None

def reset_game():
    from board import create_board
    return create_board(), 'X', False, [], False, COLUMN_COUNT // 2
