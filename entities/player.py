import pygame
from constants import *
from enum import Enum
from sound import Note
import os
import random


class PlayerState(Enum):
    LEFT = "left"
    RIGHT = "right"
    STILL = "still"
    STABBING = "stabbing"
    DEAD = "dead"
    # SHIELDING = "shielding"


class Player(pygame.sprite.Sprite):
    def reset(self):
        self.velocity: float = 0
        self.velocityx: float = 0
        self.on_ground: bool = False
        self.state: PlayerState = PlayerState.STILL
        # self.is_stabbing = False
        # self.is_shielding = False
        # self.health = True

        self.animation_timer = 0
        self.animation_speed = 8  # Adjust for animation speed
        self.current_frame = 0
        self.image = self.animations["still"][0]
        self.last_hit_time = 0

    def __init__(self) -> None:
        """Initializes the Player object."""
        super().__init__()
        self.image: pygame.Surface = pygame.Surface((60, 100))
        # self.image.fill((0, 255, 0))
        # self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        # self.rect: pygame.Rect = self.image.get_rect(center=(100, SCREEN_HEIGHT // 2))
        # self.rect = self.image.get_rect()
        # self.rect.x = x
        # self.rect.y = y
        # self.rect: pygame.Rect = self.image.get_rect(center=(100, SCREEN_HEIGHT // 2))

        self.animations = {"still": [], "walking": [], "stabbing": [], "dead": []}
        self.load_animations()

        # self.rect = self.image.get_rect()
        self.reset()
        # self.rect = self.image.get_rect(center=(100, 10))

    @property
    def is_stabbing(self):
        return self.state == PlayerState.STABBING

    def load_animations(self):
        base_path = "Tiny RPG Character Asset Pack v1.03 -Free Soldier&Orc/Characters(100x100)/Soldier/"
        frame_width = 100
        frame_height = 100
        # Still animation (using just the first frame for now)
        still_spritesheet = pygame.image.load(
            os.path.join(base_path, "Soldier/Soldier-Idle.png")
        ).convert_alpha()
        # self.animations["still"].append(still_frame)

        for i in range(6):  # 4 walking frames
            frame = still_spritesheet.subsurface(
                pygame.Rect(i * frame_width + 40, 0 + 20, 20, 40)
            )
            self.animations["still"].append(frame)

        # Walking animation
        walk_spritesheet = pygame.image.load(
            os.path.join(base_path, "Soldier/Soldier-Walk.png")
        ).convert_alpha()

        for i in range(8):  # 4 walking frames
            frame = walk_spritesheet.subsurface(
                pygame.Rect(i * frame_width + 40, 0 + 20, 20, 40)
            )
            self.animations["walking"].append(frame)

        # Stabbing animation
        stabbing_spritesheet = pygame.image.load(
            os.path.join(base_path, "Soldier/Soldier-Attack01.png")
        ).convert_alpha()

        for i in range(6):  # 3 stabbing frames
            frame = stabbing_spritesheet.subsurface(
                pygame.Rect(i * frame_width + 40, 20, 20, 40)
            )
            self.animations["stabbing"].append(frame)

        # Dead animation
        dead_spritesheet = pygame.image.load(
            os.path.join(base_path, "Soldier/Soldier-Death.png")
        ).convert_alpha()

        for i in range(4):  # 4 dead frames
            frame = dead_spritesheet.subsurface(
                pygame.Rect(i * frame_width + 40, 20, 20, 40)
            )
            self.animations["dead"].append(frame)

    def die(self):
        print("The player has died")
        self.state = PlayerState.DEAD

    def handle_note(self, note: Note) -> None:
        # self.is_stabbing = False
        # self.is_shielding = False
        if self.is_dead:
            return
        # if not self.health:
        #     print("Player is dead!")
        #     return
        if note == Note.C:
            self.jump(JUMP_POWER)
        elif note == Note.D:
            self.jump(BIG_JUMP_POWER)
        elif note == Note.A:
            self.velocityx = -MOVE_SPEED  # Move left
            self.state = PlayerState.LEFT
        elif note == Note.B:
            self.velocityx = MOVE_SPEED  # Move right
            self.state = PlayerState.RIGHT
        elif note == Note.E:
            self.stab()

    @property
    def is_dead(self):
        return self.state == PlayerState.DEAD

    def stab(self):
        if self.is_dead:
            return
        print("Stab!")
        self.state = PlayerState.STABBING
        # self.is_stabbing = True
        self.current_frame = 0

    # def shield(self):
    #     print("Shield!")
    #     self.state = PlayerState.SHIELDING
    #     self.is_shielding = True

    def update(self, platforms, enemies):
        # Horizontal movement and collision
        self.rect.x += self.velocityx
        hits_x = pygame.sprite.spritecollide(self, platforms, False)
        for hit in hits_x:
            if self.velocityx > 0:  # Moving right
                self.rect.right = hit.rect.left
            elif self.velocityx < 0:  # Moving left
                self.rect.left = hit.rect.right
            self.velocityx = 0  # Stop horizontal movement when colliding

        # Vertical movement and collision
        self.velocity += GRAVITY
        self.rect.y += self.velocity
        hits_y = pygame.sprite.spritecollide(self, platforms, False)

        for hit in hits_y:
            if self.velocity > 0:  # Falling down
                self.rect.bottom = hit.rect.top
                self.on_ground = True
            elif self.velocity < 0:  # Moving up
                self.rect.top = hit.rect.bottom
            self.velocity = 0  # Stop vertical movement when colliding

        enemy_hits = pygame.sprite.spritecollide(self, enemies, False)
        for hit in enemy_hits:
            self.velocityx = 0
            if self.velocityx > 0:
                self.rect.left = hit.rect.right
            elif self.velocityx < 0:
                self.rect.right = hit.rect.left
            if self.is_stabbing:
                hit.die()
                # hit.health = False
                # print("Enemy hit!")
            # elif self.is_shielding:
            #     print("Player shielded!")
            # else:
            #     # self.health = False
            #     self.state = PlayerState.DEAD
            #     print("Player hit!")
        # Animation update
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(
                self.animations.get(self.get_animation_key(), [self.image])
            )  # Fallback to the current image
            # self.image = self.animations.get(self.get_animation_key(), [self.image])[self.current_frame] # Fallback to the current image
            # if random.choice([True, False]):
            self.image = pygame.transform.scale(
                self.animations[self.get_animation_key()][self.current_frame], (60, 100)
            )
            # self.image = self.animations[self.get_animation_key()][self.current_frame]
            # else:
            # self.image.fill((0, 255, 0))
            # Re-adjust rect size and position
            center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = center

        if not (self.is_stabbing) and not (self.state == PlayerState.DEAD):
            if self.velocityx > 0:
                self.state = PlayerState.RIGHT
            elif self.velocityx < 0:
                self.state = PlayerState.LEFT
            else:
                self.state = PlayerState.STILL

        # if self.velocityx == 0 and self.state != PlayerState.STABBING:
        #     self.state = PlayerState.STILL

    def get_animation_key(self):
        if self.state == PlayerState.STABBING:
            return "stabbing"
        elif self.state == PlayerState.LEFT or self.state == PlayerState.RIGHT:
            return "walking"
        elif self.state == PlayerState.DEAD:
            return "dead"
        else:
            return "still"

    def jump(self, power):
        print("Jump!")
        if self.is_dead:
            return
        if self.on_ground:
            self.velocity = power
            self.on_ground = False
