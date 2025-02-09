import pygame
from constants import *
from enum import Enum
from sound import Note
import os
import random


class EnemyState(Enum):
    IDLE = "idle"
    STABBING = "stabbing"
    # SHIELDING = "shielding"
    WALKING = "walking"
    DEAD = "dead"


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, platforms, behavior, color=RED):

        super().__init__()
        self.platform_group = platforms #pygame.sprite.Group()
        # for platform_rect in platforms:
        #     platform_sprite = pygame.sprite.Sprite()
        #     platform_sprite.rect = platform_rect
        #     self.platform_group.add(platform_sprite)
        self.image: pygame.Surface = pygame.Surface((60, 100))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x_speed = 0
        self.y_speed = 0
        self.facing = "left"
        # self.health = True  # Simplified to boolean
        self.state = EnemyState.IDLE
        self.acted_this_note = False

        self.animation_timer = 0
        self.animation_speed = 8
        self.current_frame = 0
        self.animations = {"idle": [], "walking": [], "stabbing": [], "dead": []}
        self.load_animations()
        self.image = self.animations["idle"][0]

        self.behavior = behavior
        self.behavior_index = 0

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

        for i in range(8):  # 4 walking frames
            frame = walk_spritesheet.subsurface(
                pygame.Rect(i * frame_width + 40, 20, 20, 40)
            )
            self.animations["walking"].append(frame)

        stabbing_spritesheet = pygame.image.load(
            os.path.join(base_path, "Orc-Attack01.png")
        ).convert_alpha()
        for i in range(6):  # 3 stabbing frames
            frame = stabbing_spritesheet.subsurface(
                pygame.Rect(i * frame_width + 40, 20, 20, 40)
            )
            self.animations["stabbing"].append(frame)
        # Dead animation
        dead_spritesheet = pygame.image.load(
            os.path.join(base_path, "Orc-Death.png")
        ).convert_alpha()

        for i in range(4):  # 4 dead frames
            frame = dead_spritesheet.subsurface(
                pygame.Rect(i * frame_width + 40, 20, 20, 40)
            )
            self.animations["dead"].append(frame)

    def handle_note(self, note: Note):
        if not self.behavior:
            return

        self.behavior_index = (self.behavior_index + 1) % len(self.behavior)


    def update(self, player, is_note_playing):
        if not self.behavior:
            return

        if is_note_playing and not self.acted_this_note:
            if player.rect.x < self.rect.x:
                self.x_speed = -1  # Move left
                self.facing = "left"
            else:
                self.x_speed = 1  # Move right
                self.facing = "right"
            self.state = EnemyState.WALKING
            self.acted_this_note = True
        elif not is_note_playing:
            self.acted_this_note = False
            self.state = EnemyState.IDLE
            self.x_speed = 0

        # Placeholder for movement based on state
        current_action = self.behavior[self.behavior_index]

        if current_action == "stab":
            self.state = EnemyState.STABBING
            self.stab()
        # elif current_action == "shield":
        #     self.state = EnemyState.SHIELDING
        #     self.shield()
        elif current_action == "move_left":
            self.state = EnemyState.WALKING
            self.x_speed = -1
        elif current_action == "move_right":
            self.state = EnemyState.WALKING
            self.x_speed = 1
        elif current_action == "idle":
            self.state = EnemyState.IDLE
            self.x_speed = 0
        else:
            print(f"Warning: Unknown action '{current_action}'")

        self.y_speed += GRAVITY

        self.rect.x += self.x_speed
        self.on_ground = False
        # print(f"self.rect = {self.rect}")
        # print(f"self.platform_group = {self.platform_group}")
        # for p in self.platform_group:
        #     print(f"p.rect = {p.rect}")
        hits = pygame.sprite.spritecollide(self, self.platform_group, False)
        for hit in hits:
            if self.x_speed > 0:
                self.rect.right = hit.rect.left
            elif self.x_speed < 0:
                self.rect.left = hit.rect.right

            self.state = EnemyState.IDLE
            self.x_speed = 0

        self.rect.y += self.y_speed
        hits = pygame.sprite.spritecollide(self, self.platform_group, False)
        for hit in hits:
            if self.y_speed > 0:
                self.rect.bottom = hit.rect.top
                self.on_ground = True
                self.y_speed = 0
            elif self.y_speed < 0:
                self.rect.top = hit.rect.bottom
                self.y_speed = 0

        # Animation update
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(
                self.animations[self.get_animation_key()]
            )
            # self.image = self.animations[self.get_animation_key()][self.current_frame]
            # if random.choice([True, False]):
            # self.image = self.animations[self.get_animation_key()][self.current_frame]
            self.image = pygame.transform.scale(
                self.animations[self.get_animation_key()][self.current_frame], (60, 100)
            )

            # else:
            # self.image.fill((0, 255, 0))
            center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = center
    
    def get_animation_key(self):
        if self.state == EnemyState.DEAD:
            return "dead"
        elif self.state == EnemyState.WALKING:
            return "walking"
        elif self.state == EnemyState.STABBING:
            return "stabbing"
        else:
            return "idle"

    def is_stabbing(self) -> bool:
        return self.state == EnemyState.STABBING

    # def is_shielding(self) -> bool:
    #     return self.state == EnemyState.SHIELDING

    def stab(self):
        # print("Enemy stabs!")
        self.state = EnemyState.STABBING

    # def shield(self):
    #    print("Enemy shields!")
    #    self.state = EnemyState.SHIELDING
