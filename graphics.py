import pygame
from config import *
import os 
CIRCLE_MASK = pygame.Surface((SQUARESIZE - 12, SQUARESIZE - 12), pygame.SRCALPHA)
pygame.draw.circle(CIRCLE_MASK, (255, 255, 255, 255), ((SQUARESIZE - 12) // 2, (SQUARESIZE - 12) // 2), RADIUS)
CIRCLE_MASK = pygame.mask.from_surface(CIRCLE_MASK)

def load_player_disc(path, fallback_color):
    try:
        disc = pygame.image.load(path).convert_alpha()  # Giữ alpha channel (đã có nền trong suốt)
        disc = pygame.transform.smoothscale(disc, (SQUARESIZE - 12, SQUARESIZE - 12))
        return disc
    except pygame.error as e:
        print(f"Không thể tải {path}: {e}. Dùng hình mặc định.")
        disc = pygame.Surface((SQUARESIZE - 12, SQUARESIZE - 12), pygame.SRCALPHA)
        pygame.draw.circle(disc, fallback_color, ((SQUARESIZE - 12) // 2, (SQUARESIZE - 12) // 2), (SQUARESIZE - 12) // 2)
        return disc

def load_sound(path):
    if not os.path.exists(path):
        print(f"File âm thanh không tồn tại: {path}")
        return None
    try:
        sound = pygame.mixer.Sound(path)
        return sound
    except pygame.error as e:
        print(f"Lỗi khi tải âm thanh {path}: {e}")
        return None


def set_all_volumes(volume_music, volume_win, volume_fall, win_sound, fall_sound):
    pygame.mixer.music.set_volume(volume_music)
    if win_sound:
        win_sound.set_volume(volume_win)
    if fall_sound:
        fall_sound.set_volume(volume_fall)

def load_victory_image(path):
   
    try:
        img = pygame.image.load(path).convert_alpha()
        
        return img
    except pygame.error as e:
        print(f"Không thể tải ảnh thắng {path}: {e}")
        return None

def draw_board(screen, board, red_disc, yellow_disc):
    pygame.draw.rect(screen, LIGHT_BLUE, (0, SQUARESIZE, WIDTH, ROW_COUNT * SQUARESIZE))
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT):
            x = c * SQUARESIZE + SQUARESIZE // 2
            y = (r + 1) * SQUARESIZE + SQUARESIZE // 2
            pygame.draw.rect(screen, LIGHT_BLUE, (c * SQUARESIZE, (r + 1) * SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, WHITE, (x, y), RADIUS + 3)
            if board[r][c] == 'X':
                screen.blit(red_disc, (x - (SQUARESIZE - 12) // 2, y - (SQUARESIZE - 12) // 2))
            elif board[r][c] == 'O':
                screen.blit(yellow_disc, (x - (SQUARESIZE - 12) // 2, y - (SQUARESIZE - 12) // 2))
    for c in range(1, COLUMN_COUNT):
        pygame.draw.line(screen, LIGHT_BLUE, (c * SQUARESIZE, SQUARESIZE), (c * SQUARESIZE, HEIGHT - SQUARESIZE), 2)
    pygame.draw.line(screen, LIGHT_BLUE, (0, SQUARESIZE), (WIDTH, SQUARESIZE), 3)


def draw_hover_disk(screen, posx, current_player, red_disc, yellow_disc):
    
    pygame.draw.rect(screen, LIGHT_BLUE, (0, 0, WIDTH, SQUARESIZE))
    
    disc = red_disc if current_player == 'X' else yellow_disc
    
    posx = max((SQUARESIZE - 12) // 2, min(posx, WIDTH - (SQUARESIZE - 12) // 2))
    
    screen.blit(disc, (posx - (SQUARESIZE - 12) // 2, SQUARESIZE // 2 - (SQUARESIZE - 12) // 2))

def draw_turn_info(screen, current_player):
    text = f"Lượt của người chơi: {'1' if current_player == 'X' else '2'}"
    label = FONT_SMALL.render(text, True, BLACK)
    info_height = SQUARESIZE // 2
    pygame.draw.rect(screen, LIGHT_BLUE, (0, HEIGHT - SQUARESIZE, WIDTH, info_height))
    screen.blit(label, (10, HEIGHT - SQUARESIZE + 5))

def draw_reset_button(screen):
    button_height = SQUARESIZE // 2
    button_width = 140
    rect = pygame.Rect(
        WIDTH - button_width - 10,               # x: sát mép phải, cách 10px
        HEIGHT - button_height - 5,              # y: cách đáy 5px
        button_width,
        button_height
    )

    
    button_color = (220, 240, 255)      # xanh pastel
    border_color = (100, 150, 200)      # xanh viền đậm hơn
    text_color = BLACK           # xanh than


    pygame.draw.rect(screen, button_color, rect, border_radius=10)
    pygame.draw.rect(screen, border_color, rect, 2, border_radius=10)

    
    text = FONT_SMALL.render("Chơi lại", True, text_color)
    screen.blit(text, (
        rect.centerx - text.get_width() // 2,
        rect.centery - text.get_height() // 2
    ))

    return rect



def draw_game_over(screen, game_over, board, current_player):
    if game_over:
        from board import check_win  
        from utils import is_board_full

        msg = "Hòa!" if is_board_full(board) and not check_win(board, current_player) else \
              f"Người chơi {'1' if current_player == 'X' else '2'} thắng!"
        label = FONT_LARGE.render(msg, True, BLACK)
        if label.get_width() > WIDTH - 20:
            msg = "Hòa!" if is_board_full(board) else f"Người chơi {'1' if current_player == 'X' else '2'} thắng!"
            label = FONT_LARGE.render(msg, True, BLACK)
        screen.blit(label, (WIDTH // 2 - label.get_width() // 2, 10))

def draw_exit_button(screen):
    button_height = SQUARESIZE // 2
    rect = pygame.Rect(10, HEIGHT - button_height - 5, 140, button_height)

    # Màu nút
    button_color = (220, 240, 255)    
    border_color = (100, 150, 200)     
    text_color = (0, 60, 100)           

    pygame.draw.rect(screen, button_color, rect, border_radius=10)
    pygame.draw.rect(screen, border_color, rect, 2, border_radius=10)

    text = FONT_SMALL.render("Thoát game", True, text_color)
    screen.blit(text, (
        rect.centerx - text.get_width() // 2,
        rect.centery - text.get_height() // 2
    ))

    return rect

def draw_menu(screen):
    screen.fill(LIGHT_BLUE)

    title_text = FONT_LARGE.render("CONNECT 4", True, BLACK)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))

    
    play_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 60)
    pygame.draw.rect(screen, GREEN, play_button, border_radius=10)
    play_text = FONT_SMALL.render("Chơi", True, BLACK)
    screen.blit(play_text, (play_button.centerx - play_text.get_width() // 2,
                             play_button.centery - play_text.get_height() // 2))

    
    volume_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 30, 200, 60)
    pygame.draw.rect(screen, ORANGE, volume_button, border_radius=10)
    vol_text = FONT_SMALL.render("Chỉnh âm lượng", True, BLACK)
    screen.blit(vol_text, (volume_button.centerx - vol_text.get_width() // 2, volume_button.centery - vol_text.get_height() // 2))

    
    exit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 120, 200, 60)
    pygame.draw.rect(screen, (255, 80, 80), exit_button, border_radius=10)
    exit_text = FONT_SMALL.render("Thoát game", True, BLACK)
    screen.blit(exit_text, (exit_button.centerx - exit_text.get_width() // 2,
                             exit_button.centery - exit_text.get_height() // 2))

    return play_button, volume_button, exit_button


def draw_volume_settings(screen, vol_music, vol_win, vol_fall):
    screen.fill(LIGHT_BLUE)

    title = FONT_LARGE.render("Chỉnh âm lượng", True, BLACK)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 6))

    sliders = []
    labels = ["Nhạc nền", "Âm thanh thắng", "Âm thanh thả rơi"]
    volumes = [vol_music, vol_win, vol_fall]
    y_start = HEIGHT // 3
    spacing = 90

    for i, (label_text, vol) in enumerate(zip(labels, volumes)):
        label = FONT_SMALL.render(f"{label_text}: {int(vol*100)}%", True, BLACK)
        screen.blit(label, (WIDTH // 2 - 150, y_start + i*spacing - 30))

        slider_x = WIDTH // 2 - 150
        slider_y = y_start + i*spacing
        slider_width = 300
        slider_height = 9

        pygame.draw.rect(screen, DARK_GREY, (slider_x, slider_y, slider_width, slider_height), border_radius=5)
        handle_x = slider_x + int(vol * slider_width)
        handle_y = slider_y + slider_height // 2
        pygame.draw.circle(screen, PURPLE, (handle_x, handle_y), 12)

        sliders.append(((slider_x, slider_y, slider_width), handle_x))

    back_button = pygame.Rect(WIDTH // 2 - 80, HEIGHT - 100, 160, 50)
    pygame.draw.rect(screen, ORANGE, back_button, border_radius=10)
    back_text = FONT_SMALL.render("Xong", True, BLACK)
    screen.blit(back_text, (back_button.centerx - back_text.get_width() // 2,
                             back_button.centery - back_text.get_height() // 2))

    return sliders, back_button


def draw_back_button(screen):
    button_height = SQUARESIZE // 2
    rect = pygame.Rect(10, HEIGHT - button_height - 5, 140, button_height)

    # Màu nền
    button_color = (220, 240, 255)
    border_color = (100, 150, 200)
    text_color = BLACK

    pygame.draw.rect(screen, button_color, rect, border_radius=10)
    pygame.draw.rect(screen, border_color, rect, 2, border_radius=10)

    text = FONT_SMALL.render("Menu", True, text_color)
    screen.blit(text, (
        rect.centerx - text.get_width() // 2,
        rect.centery - text.get_height() // 2
    ))

    return rect
