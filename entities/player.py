import pygame
from constants import *
from enum import Enum
from sound import Note


class PlayerState(Enum):
    LEFT = "left"
    RIGHT = "right"
    STILL = "still"


class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        """Initializes the Player object."""
        super().__init__()
        self.image: pygame.Surface = pygame.Surface((30, 50))
        self.image.fill((0, 255, 0))
        self.rect: pygame.Rect = self.image.get_rect(center=(100, SCREEN_HEIGHT // 2))
        self.velocity: float = 0
        self.velocityx: float = 0
        self.on_ground: bool = False
        self.current_state: PlayerState = (
            PlayerState.STILL
        )  # Initialize action attribute

    def handle_note(self, note: Note) -> None:
        if note == Note.C:
            self.jump(JUMP_POWER)
        elif note == Note.D:
            self.jump(BIG_JUMP_POWER)
        elif note == Note.A:
            self.velocityx += MOVE_SPEED
            # self.current_state = PlayerState.LEFT
        elif note == Note.B:
            self.velocityx -= MOVE_SPEED
            # self.current_state = PlayerState.RIGHT

    def update(self, platforms):
        # Horizontal movement
        # if hasattr(self, 'current_action'):
        # if self.current_state == PlayerState.LEFT:
        #     self.velocityx += MOVE_SPEED
        # elif self.current_state == PlayerState.RIGHT:
        #     self.velocityx -= MOVE_SPEED
        self.rect.x += self.velocityx
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
