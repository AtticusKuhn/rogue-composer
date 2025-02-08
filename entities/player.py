import pygame
from constants import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 50))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(center=(100, SCREEN_HEIGHT//2))
        self.velocity = 0
        self.on_ground = False
        self.current_action = None  # Initialize action attribute

    def update(self, platforms):
        # Horizontal movement
        if hasattr(self, 'current_action'):
            if self.current_action == 'a':
                self.rect.x += MOVE_SPEED
            elif self.current_action == 'b':
                self.rect.x -= MOVE_SPEED

        # Vertical movement
        self.velocity += GRAVITY
        self.rect.y += self.velocity

        # Platform collision
        self.on_ground = False
        hits = pygame.sprite.spritecollide(self, platforms, False)
        for hit in hits:
            if self.velocity > 0:
                self.rect.bottom = hit.rect.top
                self.velocity = 0
                self.on_ground = True
            elif self.velocity < 0:
                self.rect.top = hit.rect.bottom
                self.velocity = 0

    def jump(self, power):
        if self.on_ground:
            self.velocity = power
            self.on_ground = False
