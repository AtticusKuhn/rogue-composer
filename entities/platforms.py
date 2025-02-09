import pygame
from constants import *


class Platform(pygame.sprite.Sprite):
    _platform_image = None  # Class-level cache for the sprite sheet

    def __init__(self, x: int, y: int, w: int, h: int):
        super().__init__()
        # Load sprite sheet once and cache it
        if Platform._platform_image is None:
            Platform._platform_image = pygame.image.load(
                'brackeys_platformer_assets/sprites/platforms.png'
            ).convert_alpha()
            
        # Extract grass sprite from coordinates (0,0) to (10,50)
        grass_sprite = Platform._platform_image.subsurface(pygame.Rect(0, 0, 50, 10))
        # Scale sprite to match platform dimensions
        self.image = pygame.transform.scale(grass_sprite, (w, h))
        self.rect = self.image.get_rect(topleft=(x, y))
