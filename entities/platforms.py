import pygame
from constants import *

class Platform(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, w: int, h: int):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill((100, 100, 100))
        self.rect = self.image.get_rect(topleft=(x, y))
