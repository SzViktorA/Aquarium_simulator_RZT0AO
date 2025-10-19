import pygame
import random

class Bubble_VS:
    def __init__(self, x, y, radius=None, speed=None):
        self.x = float(x)
        self.y = float(y)
        self.radius = radius if radius is not None else random.randint(4, 12)
        self.speed = speed if speed is not None else random.uniform(0.4, 1.6)
        self.alpha = random.randint(160, 230)

    def update(self):
        self.y -= self.speed
        self.alpha -= 0.6
        if self.alpha < 0:
            self.alpha = 0

    def draw(self, screen):
        surf = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        col = (200, 220, 255, int(self.alpha))
        pygame.draw.circle(surf, col, (self.radius, self.radius), self.radius)
        pygame.draw.circle(surf, (240, 245, 255, int(self.alpha * 0.6)), (self.radius, self.radius), max(1, self.radius - 1), 1)
        screen.blit(surf, (int(self.x - self.radius), int(self.y - self.radius)))

    def is_dead(self, screen_height):
        return (self.y + self.radius) < 0 or self.alpha <= 1
