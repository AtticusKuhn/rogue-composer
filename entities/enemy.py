import pygame
from constants import *
from enum import Enum


class EnemyState(Enum):
    IDLE = "idle"
    STABBING = "stabbing"
    SHIELDING = "shielding"


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color=RED):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x_speed = 0
        self.y_speed = 0
        self.facing = "left"
        self.health = True  # Simplified to boolean
        self.state = EnemyState.IDLE
        self.acted_this_note = False

    def update(self, player, is_note_playing):
        if is_note_playing and not self.acted_this_note:
            # Placeholder for AI decision-making
            self.state = EnemyState.STABBING  # Default action for now
            self.acted_this_note = True
        elif not is_note_playing:
            self.acted_this_note = False
            self.state = EnemyState.IDLE

        # Placeholder for movement based on state
        if self.state == EnemyState.STABBING:
            self.stab()
        elif self.state == EnemyState.SHIELDING:
            self.shield()
    def is_stabbing(self) -> bool:
        return self.state == EnemyState.STABBING
    def stab(self):
        print("Enemy stabs!")
        self.state = EnemyState.STABBING

    def shield(self):
        print("Enemy shields!")
        self.state = EnemyState.SHIELDING
