import pygame
from constants import *

class Apple(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.sprite_sheet = pygame.image.load("Free/Items/Fruits/Apple.png")
        self.animation_frames = 17
        self.current_frame = 0
        self.animation_timer = 0
        self.frames = self.load_frames()  # Load frames
        self.image = self.frames[self.current_frame] # Initialize image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.is_collected = False


    def load_frames(self):
        frames = []
        width, height = self.sprite_sheet.get_size()
        frame_width = width // self.animation_frames
        frame_height = height

        for i in range(self.animation_frames):
            frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            frame.blit(self.sprite_sheet, (0, 0), (i * frame_width, 0, frame_width, frame_height))
            frames.append(frame)
        return frames

    def update(self, player):
        # Basic animation
        self.animation_timer += 1
        if self.animation_timer > 5:
          self.animation_timer = 0
          self.current_frame = (self.current_frame + 1) % self.animation_frames
          self.image = self.frames[self.current_frame]  # Update the image

        # Collision detection
        if self.rect.colliderect(player.rect):
            # Placeholder for win condition
            print("Player touched the apple!")
            self.is_collected = True
            return True
        return False
