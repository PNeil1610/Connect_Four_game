import pygame
from graphics import load_player_disc, load_sound
from config import RED, YELLOW
from paths import resource_path

def load_assets(resource_path):
    p1 = load_player_disc(resource_path('assets/tao.png'), RED)
    p2 = load_player_disc(resource_path('assets/khe.png'), YELLOW)
    win = load_sound(resource_path('assets/tungho.mp3'))
    fall = load_sound(resource_path('assets/tharoi.mp3'))
    return p1, p2, win, fall
