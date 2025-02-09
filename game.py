import pygame
import sys
from entities.player import Player
from entities.apple import Apple
from levels import levels
# from entities.player import Player
from entities.enemy import Enemy
from entities.platforms import Platform
from sound import SoundManager, Note, toNote
from constants import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.BACKGROUND_IMAGE = pygame.image.load("Forest.png").convert()
        pygame.display.set_caption("Synesthesia")
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()  # New enemy group
        self.apples = pygame.sprite.Group()
        self.font = pygame.font.Font(None, 36)
        self.cursor = -1
        self.level_index = 0
        # Note positions (mapping notes to vertical positions)
        self.note_positions = {
            Note.A: SCREEN_HEIGHT - 100,
            Note.B: SCREEN_HEIGHT - 120,
            Note.C: SCREEN_HEIGHT - 140,
            Note.D: SCREEN_HEIGHT - 160,
            Note.E: SCREEN_HEIGHT - 180,
            Note.F: SCREEN_HEIGHT - 200,
            Note.G: SCREEN_HEIGHT - 220,
        }

        self.sound_manager = SoundManager()

        # Load level data
        level_data = levels[self.level_index]

        # Create platforms
        for platform_data in level_data["platforms"]:
            platform = Platform(
                platform_data["x"],
                platform_data["y"],
                platform_data["width"],
                platform_data["height"],
            )
            self.platforms.add(platform)

        # Calculate player's starting y-position to be on top of the first platform
        player_start_y = level_data["platforms"][0]["y"] - 300
        self.player = Player()
        self.player.rect.center = (100, player_start_y)
        self.player.last_hit_time = 0

        # Create enemies
        for enemy_data in level_data["enemies"]:
            enemy = Enemy(
                enemy_data["x"],
                enemy_data["y"],
                enemy_data["width"],
                enemy_data["height"],
                platforms=self.platforms,
                color=eval(enemy_data["color"]),
            )
            self.enemies.add(enemy)
            enemy.last_hit_time = 0

        # Create apples
        for apple_data in level_data["apples"]:
            apple = Apple(apple_data["x"], apple_data["y"])
            self.apples.add(apple)

        self.all_sprites.add(self.player, *self.platforms, *self.enemies, *self.apples)

        self.input_sequence = []
        self.playing_sequence = False
        self.is_note_playing = False  # Flag for note playing

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if not self.playing_sequence:
                    if event.unicode in "abcdefg":
                        note = toNote(event.unicode)
                        self.input_sequence.append(note)
                        self.sound_manager.play_note(note)
                    elif event.key == pygame.K_SPACE:
                        self.playing_sequence = True
                        self.execute_sequence()

            if event.type == pygame.USEREVENT:
                self.execute_sequence()

    def execute_sequence(self):
        if self.cursor < len(self.input_sequence) - 1:
            self.cursor += 1
            current_note = self.input_sequence[self.cursor]
            self.player.handle_note(current_note)
            for enemy in self.enemies:
                enemy.handle_note(current_note)
            self.sound_manager.play_note(current_note)
            self.is_note_playing = True  # Set flag
            # Queue next action
            pygame.time.set_timer(pygame.USEREVENT, 500)
        else:
            pygame.time.set_timer(pygame.USEREVENT, 0)
            self.playing_sequence = False
            self.is_note_playing = False  # Reset flag

    def load_level(self):
        # Reset game state
        self.all_sprites.empty()
        self.platforms.empty()
        self.enemies.empty()
        self.apples.empty()
        self.input_sequence = []
        self.cursor = -1
        self.playing_sequence = False

        # Load level data
        level_data = levels[self.level_index]

        # Create platforms
        for platform_data in level_data["platforms"]:
            platform = Platform(
                platform_data["x"],
                platform_data["y"],
                platform_data["width"],
                platform_data["height"],
            )
            self.platforms.add(platform)

        # Calculate player's starting y-position
        player_start_y = level_data["platforms"][0]["y"] - 300
        self.player.rect.center = (100, player_start_y)
        self.player.last_hit_time = 0

        # Create enemies
        for enemy_data in level_data["enemies"]:
            enemy = Enemy(
                enemy_data["x"],
                enemy_data["y"],
                enemy_data["width"],
                enemy_data["height"],
                platforms=self.platforms,
                color=eval(enemy_data["color"]),
            )
            self.enemies.add(enemy)
            enemy.last_hit_time = 0

        # Create apples
        for apple_data in level_data["apples"]:
            apple = Apple(apple_data["x"], apple_data["y"])
            self.apples.add(apple)

        self.all_sprites.add(self.player, *self.platforms, *self.enemies, *self.apples)

    def draw_note(self, note, position, cursor):
        # Draw five horizontal lines for the staff
        staff_start_y = SCREEN_HEIGHT - 250
        staff_line_spacing = 20
        for i in range(5):
            pygame.draw.line(
                self.screen,
                (255, 255, 255),
                (0, staff_start_y + i * staff_line_spacing),
                (SCREEN_WIDTH, staff_start_y + i * staff_line_spacing),
                2,
            )

        # Calculate note position on the staff
        x = 10 + position * 60
        note_positions = {  # relative to staff_start_y
            Note.A: staff_start_y + staff_line_spacing * 3.5,
            Note.B: staff_start_y + staff_line_spacing * 3, # on space below
            Note.C: staff_start_y + staff_line_spacing * 2.5,  # on space above
            Note.D: staff_start_y + staff_line_spacing * 2,
            Note.E: staff_start_y + staff_line_spacing * 1.5,
            Note.F: staff_start_y + staff_line_spacing * 1,
            Note.G: staff_start_y + staff_line_spacing * 0.5,
            
        }

        y = note_positions.get(note, staff_start_y)

        color = (0, 255, 0) if cursor == position else (255, 255, 255)
        pygame.draw.circle(self.screen, color, (x, int(y)), 10)

        # Draw stem
        stem_length = 30
        staff_middle_y = staff_start_y + staff_line_spacing * 2  # 3rd line
        if y > staff_middle_y:
            stem_start_x = x + 10
            stem_start_y = y
            stem_end_x = x + 10
            stem_end_y = y - stem_length
        else:
            stem_start_x = x - 10
            stem_start_y = y
            stem_end_x = x - 10
            stem_end_y = y + stem_length

        pygame.draw.line(self.screen, color, (stem_start_x, int(stem_start_y)), (stem_end_x, int(stem_end_y)), 2)

    def run(self):
        while True:
            self._handle_events()
            # Update player
            self.player.update(self.platforms, self.enemies)

            # Update enemies
            for enemy in self.enemies:
                enemy.update(self.player, self.is_note_playing)

            # Handle apple collection
            for apple in self.apples:
                if apple.update(self.player):
                    print("Level Won!")
                    self.level_index += 1
                    if self.level_index < len(levels):
                        self.load_level()
                    else:
                        print("Game Won!")
                        # TODO: Implement proper game completion screen/logic
                        # For now, just quit the game
                        pygame.quit()
                        sys.exit()

            # Handle collisions
            current_time = pygame.time.get_ticks()
            for enemy in self.enemies:
                if pygame.sprite.collide_rect(self.player, enemy):
                    if self.player.is_stabbing:
                        enemy.health = False  # Enemy takes damage
                        enemy.last_hit_time = current_time
                    if enemy.is_stabbing() and (current_time - self.player.last_hit_time) > 500:
                        self.player.health = False  # Player takes damage
                        self.player.last_hit_time = current_time

            # Remove dead sprites
            dead_sprites = [
                sprite
                for sprite in self.all_sprites
                if hasattr(sprite, "health") and not sprite.health
            ]
            for sprite in dead_sprites:
                self.all_sprites.remove(sprite)
                if sprite in self.enemies:
                    self.enemies.remove(sprite)

            # Drawing
            self.screen.fill((0, 0, 0))  # Clear screen
            background_image = pygame.image.load("background_image.png")
            self.screen.blit(
                pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT)),
                (0, 0),
            )
            # Draw player
            if self.player.facing == "right":
                self.screen.blit(self.player.image, self.player.rect)
            else:
                self.screen.blit(pygame.transform.flip(self.player.image,
                                                       True, False), self.player.rect)

            # Draw enemies
            for enemy in self.enemies:
                if enemy.facing == "right":
                    self.screen.blit(enemy.image, enemy.rect)
                
                else:
                    self.screen.blit(pygame.transform.flip(enemy.image, True, False), enemy.rect)

            # Draw platforms
            for platform in self.platforms:
                self.screen.blit(platform.image, platform.rect)

            # Draw apples
            for apple in self.apples:
                if not apple.is_collected:
                    self.screen.blit(apple.image, apple.rect)

            # self.all_sprites.draw(self.screen) # No longer needed

            # Draw input sequence
            for i, note in enumerate(self.input_sequence):
                self.draw_note(note, i, self.cursor)

            pygame.display.flip()
            self.clock.tick(60)
