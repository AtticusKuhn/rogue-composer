import pygame
from pygame.sprite import Sprite
from constants import PLATFORM_COLOR

class Platform(Sprite):
    """Represents a collidable platform surface."""
    
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(PLATFORM_COLOR)
        self.rect = self.image.get_rect(topleft=(x, y))
