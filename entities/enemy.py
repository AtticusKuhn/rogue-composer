import pygame
from constants import *

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
        self.health = 100

    def update(self, player):
        # Basic AI: Move towards the player
        if player:
            if player.rect.x < self.rect.x:
                self.x_speed = -ENEMY_SPEED
                self.facing = "left"
            elif player.rect.x > self.rect.x:
                self.x_speed = ENEMY_SPEED
                self.facing = "right"
            else:
                self.x_speed = 0

            # Simple collision handling (stop at platforms)
            self.rect.x += self.x_speed

            # Keep within screen bounds
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > SCREEN_WIDTH:
                self.rect.right = SCREEN_WIDTH

    def stab(self):
        print("Enemy stabs!")
        stab_damage = 10
        stab_range = 50
        
        # Create a rect for the stab attack
        if self.facing == "right":
            stab_rect = pygame.Rect(self.rect.right, self.rect.centery - 10, stab_range, 20)
        else:
            stab_rect = pygame.Rect(self.rect.left - stab_range, self.rect.centery - 10, stab_range, 20)

        # Check for collision with the player
        if player and stab_rect.colliderect(player.rect):
            player.health -= stab_damage
            print(f"Player hit! Health: {player.health}")

    def shield(self):
        print("Enemy shields!")
        # Implement shield logic (e.g., reduce damage taken)
