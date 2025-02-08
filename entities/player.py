import pygame
from typing import List
from pygame.sprite import Sprite, Group
from constants import GRAVITY, MOVE_SPEED, JUMP_POWER, BIG_JUMP_POWER, Action

class Player(Sprite):
    """Represents the player character with physics-based movement."""
    
    def __init__(self, start_pos: tuple[int, int]):
        super().__init__()
        self.image = pygame.Surface((30, 50))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(center=start_pos)
        self.velocity: float = 0.0
        self.on_ground: bool = False
        self.current_action: Action = None

    def update(self, platforms: Group) -> None:
        """Update player position and state based on current action and physics.
        
        Args:
            platforms: Group of platform sprites to check collisions against
        """
        self._handle_horizontal_movement()
        self._apply_gravity()
        self._handle_vertical_collision(platforms)

    def _handle_horizontal_movement(self) -> None:
        """Process horizontal movement based on current action."""
        if self.current_action == Action.MOVE_LEFT:
            self.rect.x -= MOVE_SPEED
        elif self.current_action == Action.MOVE_RIGHT:
            self.rect.x += MOVE_SPEED

    def _apply_gravity(self) -> None:
        """Apply gravity force and update vertical position."""
        self.velocity += GRAVITY
        self.rect.y += self.velocity

    def _handle_vertical_collision(self, platforms: Group) -> None:
        """Detect and resolve collisions with platforms.
        
        Args:
            platforms: Group of platform sprites to check against
        """
        self.on_ground = False
        for platform in pygame.sprite.spritecollide(self, platforms, False):
            if self.velocity > 0:  # Falling
                self.rect.bottom = platform.rect.top
                self.velocity = 0
                self.on_ground = True
            elif self.velocity < 0:  # Rising
                self.rect.top = platform.rect.bottom
                self.velocity = 0

    def jump(self, power: float) -> None:
        """Initiate jump if player is on ground.
        
        Args:
            power: Vertical velocity to apply (negative for upward movement)
        """
        if self.on_ground:
            self.velocity = power
            self.on_ground = False
