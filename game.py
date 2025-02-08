import pygame
import sys
from entities.player import Player
from entities.platforms import Platform
from sound import SoundManager
from constants import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Synesthesia")
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.font = pygame.font.Font(None, 36)

        # Note positions (mapping notes to vertical positions)
        self.note_positions = {
            'a': SCREEN_HEIGHT - 100,
            'b': SCREEN_HEIGHT - 120,
            'c': SCREEN_HEIGHT - 140,
            'd': SCREEN_HEIGHT - 160,
            'e': SCREEN_HEIGHT - 180,
            'f': SCREEN_HEIGHT - 200,
            'g': SCREEN_HEIGHT - 220,
        }

        self.sound_manager = SoundManager()

        # Create ground platform
        self.platforms.add(Platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40))
        self.player = Player()
        self.all_sprites.add(self.player, *self.platforms)

        self.input_sequence: list[str] = []
        self.playing_sequence: bool = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if not self.playing_sequence:
                    if event.unicode in 'abcdefg':
                        self.input_sequence.append(event.unicode)
                    elif event.key == pygame.K_SPACE:
                        self.playing_sequence = True
                        self.execute_sequence()

            if event.type == pygame.USEREVENT:
                self.execute_sequence()

    def execute_sequence(self):
        if self.input_sequence:
            current_note = self.input_sequence.pop(0)
            self.player.current_action = current_note
            self.sound_manager.play_note(current_note)

            # Handle actions
            if current_note == 'c':
                self.player.jump(JUMP_POWER)
            elif current_note == 'd':
                self.player.jump(BIG_JUMP_POWER)

            # Queue next action
            if self.input_sequence:
                pygame.time.set_timer(pygame.USEREVENT, 500)
            else:
                pygame.time.set_timer(pygame.USEREVENT, 0)
                self.playing_sequence = False

    def draw_note(self, note, position):
        """Draws a note on the screen."""
        x = 10 + position * 60  # Horizontal spacing
        y = self.note_positions.get(note, SCREEN_HEIGHT - 100)  # Default to 'a' position
        pygame.draw.rect(self.screen, (255, 255, 255), (x, y, 40, 20))

    def run(self):
        while True:
            self.handle_events()
            self.player.update(self.platforms)

            self.screen.fill((0, 0, 0))
            self.all_sprites.draw(self.screen)

            # Draw input sequence
            for i, note in enumerate(self.input_sequence):
                self.draw_note(note, i)

            pygame.display.flip()
            self.clock.tick(60)
