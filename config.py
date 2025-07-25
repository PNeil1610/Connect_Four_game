import pygame

# Kích thước
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 90
RADIUS = int(SQUARESIZE / 2 - 6)
WIDTH = COLUMN_COUNT * SQUARESIZE
HEIGHT = (ROW_COUNT + 2) * SQUARESIZE

# Màu sắc
BLUE = (0, 0, 255)
PINK = (255, 192, 203)
PURPLE = (128, 0, 128)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
GREEN = (0, 255, 0)
LIGHT_BLUE = (173, 216, 230)
DARK_GREY = (64, 64, 64)
# Font
pygame.font.init()
FONT_LARGE = pygame.font.SysFont("Segoe UI", 36)
FONT_SMALL = pygame.font.SysFont("Segoe UI", 24)