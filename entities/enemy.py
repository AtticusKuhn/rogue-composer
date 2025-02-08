import pygame
from constants import *
from enum import Enum
from sound import Note
import os
import random
class EnemyState(Enum):
    IDLE = "idle"
    STABBING = "stabbing"
    SHIELDING = "shielding"
    WALKING = "walking"


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color=RED):
        super().__init__()
        self.image = pygame.Surface([60, 100])
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

        self.animation_timer = 0
        self.animation_speed = 8
        self.current_frame = 0
        self.animations = {
            "idle": [],
            "walking": [],
        }
        self.load_animations()
        self.image = self.animations["idle"][0]


    def load_animations(self):
        base_path = "Tiny RPG Character Asset Pack v1.03 -Free Soldier&Orc/Characters(100x100)/Orc/Orc/"

        # Idle animation (using just the first frame for now)
        frame_width = 100
        frame_height = 100
        still_spritesheet = pygame.image.load(
            os.path.join(base_path, "Orc-Idle.png")
        ).convert_alpha()
        # self.animations["still"].append(still_frame)

        for i in range(6):  # 6 still frames
            frame = still_spritesheet.subsurface(
                pygame.Rect(i * frame_width + 40, 20, 20, 40)
            )
            self.animations["idle"].append(frame)
        # idle_frame = pygame.image.load(os.path.join(base_path, "Orc-Idle.png")).convert_alpha()
        # self.animations["idle"].append(idle_frame)

        # Walking animation
        # for i in range(1, 5):  # Assuming 4 walking frames
        #     filename = f"Orc-Walk{i}.png"
        #     path = os.path.join(base_path, filename)
        #     frame = pygame.image.load(path).convert_alpha()
        #     self.animations["walking"].append(frame)
        walk_spritesheet = pygame.image.load(
            os.path.join(base_path, "Orc-Walk.png")
        ).convert_alpha()
       

        for i in range(4):  # 4 walking frames
            frame = walk_spritesheet.subsurface(
                pygame.Rect(i * frame_width + 40, 20, 20, 40)
            )
            self.animations["walking"].append(frame)

    def handle_note(self, note: Note):
        if self.state == EnemyState.STABBING:
            self.state = EnemyState.IDLE
        if self.state == EnemyState.IDLE:
            self.state = EnemyState.SHIELDING
        if self.state == EnemyState.SHIELDING:
            self.state = EnemyState.STABBING

    def update(self, player, is_note_playing):
        if is_note_playing and not self.acted_this_note:
            # Placeholder for AI decision-making
            #self.state = EnemyState.STABBING  # Default action for now
            self.x_speed = -1 #move towards the player
            self.state = EnemyState.WALKING
            self.acted_this_note = True
        elif not is_note_playing:
            self.acted_this_note = False
            self.state = EnemyState.IDLE
            self.x_speed = 0

        # Placeholder for movement based on state
        if self.state == EnemyState.STABBING:
            self.stab()
        elif self.state == EnemyState.SHIELDING:
            self.shield()

        self.rect.x += self.x_speed

        # Animation update
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.animations[self.get_animation_key()])
            # self.image = self.animations[self.get_animation_key()][self.current_frame]
            if random.choice([True, False]):
                self.image = self.animations[self.get_animation_key()][self.current_frame]
            else:
                self.image.fill((0, 255, 0))
            center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = center
          
    def get_animation_key(self):
        if self.state == EnemyState.WALKING:
            return "walking"
        else:
            return "idle"

    def is_stabbing(self) -> bool:
        return self.state == EnemyState.STABBING

    def is_shielding(self) -> bool:
        return self.state == EnemyState.SHIELDING

    def stab(self):
        print("Enemy stabs!")
        self.state = EnemyState.STABBING

    def shield(self):
        print("Enemy shields!")
        self.state = EnemyState.SHIELDING
