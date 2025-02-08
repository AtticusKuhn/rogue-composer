import pygame
from constants import *
from enum import Enum
from sound import Note


class PlayerState(Enum):
    LEFT = "left"
    RIGHT = "right"
    STILL = "still"
    STABBING = "stabbing"
    SHIELDING = "shielding"


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
        self.current_state: PlayerState = PlayerState.STILL
        self.is_stabbing = False
        self.is_shielding = False
        self.health = True

    def handle_note(self, note: Note) -> None:
        if note == Note.C:
            self.jump(JUMP_POWER)
        elif note == Note.D:
            self.jump(BIG_JUMP_POWER)
        elif note == Note.A:
            self.velocityx += MOVE_SPEED
            self.current_state = PlayerState.LEFT
        elif note == Note.B:
            self.velocityx -= MOVE_SPEED
            self.current_state = PlayerState.RIGHT
        elif note == Note.E:
            self.stab()
        elif note == Note.F:
            self.shield()

    def stab(self):
        print("Stab!")
        self.current_state = PlayerState.STABBING
        self.is_stabbing = True

    def shield(self):
        print("Shield!")
        self.current_state = PlayerState.SHIELDING
        self.is_shielding = True
        
    def update(self, platforms):
        # Reset stab and shield state
        self.is_stabbing = False
        self.is_shielding = False
        # Horizontal movement
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
