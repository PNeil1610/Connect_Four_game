import random
import pygame

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-4, -2)
        self.alpha = 255
        self.radius = random.randint(6, 10)
        self.color = random.choice([
            (255, 255, 255), (255, 200, 0), (255, 50, 50),
            (50, 150, 255), (255, 0, 255), (0, 255, 150),
        ])

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.05
        self.alpha -= 2
        self.alpha = max(self.alpha, 0)

    def draw(self, screen):
        if self.alpha > 0:
            s = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
            pygame.draw.circle(s, self.color + (self.alpha,), (self.radius, self.radius), self.radius)
            screen.blit(s, (self.x - self.radius, self.y - self.radius))
