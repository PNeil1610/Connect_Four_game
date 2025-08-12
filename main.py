import asyncio
import platform
import pygame
import sys
import random
from config import *
from board import create_board, drop_disc, check_win
from utils import is_board_full
from graphics import*
from effects import Particle
from assets_loader import load_assets
from game_logic import*
from paths import resource_path


if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding='utf-8')

async def main():
    pygame.init()
    game_state = "menu"
# âm thanh
    volume = 0.5
    volume_music = 0.5
    volume_win = 0.5
    volume_fall = 0.5
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.init()
    dragging_volume = False
    pygame.mixer.music.load(resource_path("assets/nhacnen.mp3"))
    pygame.mixer.music.set_volume(volume_music)
    pygame.mixer.music.play(-1) 
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Connect 4")
    Player1_DISC, Player2_DISC, WIN_SOUND, FALLING_SOUND = load_assets(resource_path)
    set_all_volumes(volume, volume_win, volume_fall, WIN_SOUND, FALLING_SOUND)

    board = create_board()
    current_player = 'X'
    game_over = False
    col = COLUMN_COUNT // 2
    dropping = False
    drop_row = 0
    drop_col = 0
    drop_y = SQUARESIZE // 2
    particles = []

    clock = pygame.time.Clock()
    dragging_volume = False
    while True:
        if game_state == "menu":
            play_button, volume_button, exit_button = draw_menu(screen)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.FINGERDOWN:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = event.pos
                    else:
                        x = event.x * WIDTH
                        y = event.y * HEIGHT

                    if play_button.collidepoint(x, y):
                        game_state = "playing"
                    elif volume_button.collidepoint(x, y):
                        game_state = "volume_settings"
                    elif exit_button.collidepoint(x, y):
                        pygame.quit()
                        sys.exit()

            await asyncio.sleep(1.0 / 60)
            continue

        elif game_state == "volume_settings":
            sliders, back_button = draw_volume_settings(screen, volume_music, volume_win, volume_fall)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.FINGERDOWN):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = event.pos
                    else:
                        x = event.x * WIDTH
                        y = event.y * HEIGHT

                    if back_button.collidepoint(x, y):
                        game_state = "menu"

                    for i, (slider_rect, handle_x) in enumerate(sliders):
                        if abs(x - handle_x) <= 12 and abs(y - slider_rect[1]) <= 20:
                            dragging_volume = i  # 0: music, 1: win, 2: fall

                elif event.type == pygame.MOUSEBUTTONUP:
                    dragging_volume = None

                elif (event.type in (pygame.MOUSEMOTION, pygame.FINGERMOTION)) and dragging_volume is not None:
                    if event.type == pygame.MOUSEMOTION:
                        x, y = event.pos
                    else:
                        x = event.x * WIDTH
                        y = event.y * HEIGHT

                    slider_x, slider_y, slider_width = sliders[dragging_volume][0]
                    new_x = max(slider_x, min(x, slider_x + slider_width))
                    new_vol = (new_x - slider_x) / slider_width

                    if dragging_volume == 0:
                        volume_music = new_vol
                    elif dragging_volume == 1:
                        volume_win = new_vol
                    elif dragging_volume == 2:
                        volume_fall = new_vol

                    set_all_volumes(volume_music, volume_win, volume_fall, WIN_SOUND, FALLING_SOUND)
        if game_state == "playing":
            clock.tick(120)
            for event in pygame.event.get():#chuỗi sự kiện
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # elif event.type == pygame.MOUSEMOTION and not game_over and not dropping:
                #     x, y = event.pos
                #     col = x // SQUARESIZE if SQUARESIZE <= y < HEIGHT - SQUARESIZE else None
                elif (event.type == pygame.MOUSEMOTION or event.type == pygame.FINGERMOTION) and not game_over and not dropping:
                    x, y = event.pos
                    # Chỉ cập nhật col nếu chuột nằm trong khu vực ngang của bàn cờ
                    if 0 <= x <= WIDTH:
                        col = x // SQUARESIZE
                    else:
                        col = None
                elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.FINGERDOWN:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = event.pos
                    elif event.type == pygame.FINGERDOWN:
                        x = event.x * WIDTH
                        y = event.y * HEIGHT
                    res = handle_input(x, y, screen, board, current_player, game_over, dropping)
                    if back_rect.collidepoint(x, y):
                        # Quay về menu và reset game
                        board, current_player, game_over, particles, dropping, col = reset_game()
                        game_state = "menu"
                        continue


                    if res == "reset":
                        if WIN_SOUND:
                            WIN_SOUND.stop()
                        board, current_player, game_over, particles, dropping, col = reset_game()
                    elif res:
                        drop_row, drop_col = res
                        dropping = True
                        drop_y = SQUARESIZE // 2
                        col = None
            if dropping:
                target_y = (drop_row + 1) * SQUARESIZE + SQUARESIZE // 2
                drop_y += 10
                if drop_y >= target_y:
                    drop_y = target_y
                    dropping = False
                    if FALLING_SOUND:
                        FALLING_SOUND.play()
                    drop_disc(board, drop_col, current_player)
                    if check_win(board, current_player):
                        game_over = True
                        if WIN_SOUND:
                            WIN_SOUND.play()
                            WIN_SOUND.fadeout(3000)
                        for _ in range(50):
                            particles.append(Particle(WIDTH // 2, HEIGHT // 2))
                    elif is_board_full(board):
                        game_over = True
                    else:
                        current_player = 'O' if current_player == 'X' else 'X'
            if not dropping and not game_over:
                # Nếu chưa rê chuột thì col vẫn None, ta đặt mặc định là giữa
                if col is None:
                    col = COLUMN_COUNT // 2
            screen.fill(LIGHT_BLUE)
            draw_board(screen, board, Player1_DISC, Player2_DISC)
            if not game_over and not dropping and col is not None:
                disc_x = col * SQUARESIZE + SQUARESIZE // 2
                draw_hover_disk(screen, disc_x, current_player, Player1_DISC, Player2_DISC)
            elif dropping:
                disc_x = drop_col * SQUARESIZE + SQUARESIZE // 2
                disc = Player1_DISC if current_player == 'X' else Player2_DISC
                screen.blit(disc, (disc_x - (SQUARESIZE - 12) // 2, drop_y - (SQUARESIZE - 12) // 2))

            for particle in particles[:]:
                particle.update()
                particle.draw(screen)
                if particle.alpha <= 0:
                    particles.remove(particle)


            draw_turn_info(screen, current_player)
            button_rect = draw_reset_button(screen)
            back_rect = draw_back_button(screen)
            draw_game_over(screen, game_over, board, current_player)
            pygame.display.update()
            await asyncio.sleep(1.0 / 120)

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())