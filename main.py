import pygame
import sys
import numpy as np
from entities.player import Player
from entities.platforms import Platform
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

        # Initialize Pygame's mixer
        pygame.mixer.init(frequency=SAMPLE_RATE, size=-16, channels=2, buffer=512)

        # Create a dictionary to store the pre-generated tones
        self.note_sounds = {
            'a': generate_tone(440),   # A4
            'b': generate_tone(494),   # B4
            'c': generate_tone(523),   # C5
            'd': generate_tone(587),   # D5
            'e': generate_tone(659),   # E5
            'f': generate_tone(698),   # F5
            'g': generate_tone(784)    # G5
        }

        # Create ground platform
        ground = Platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40)
        self.platforms.add(ground)
        self.player = Player()
        self.all_sprites.add(self.player, *self.platforms)

        self.input_sequence = []
        self.playing_sequence = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if not self.playing_sequence:
                    if event.unicode in 'abcdefg':
                        self.input_sequence.append(event.unicode)
                        # Play the corresponding sound
                        pygame.mixer.Sound(self.note_sounds[event.unicode]).play()
                    elif event.key == pygame.K_SPACE:
                        self.playing_sequence = True
                        self.execute_sequence()

            if event.type == pygame.USEREVENT:
                self.execute_sequence()


    def execute_sequence(self):
        if self.input_sequence:
            current_note = self.input_sequence.pop(0)
            self.player.current_action = current_note

            # Play corresponding sound
            pygame.mixer.Sound(self.note_sounds[current_note]).play()

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

    def run(self):
        while True:
            self.handle_events()
            self.player.update(self.platforms)

            self.screen.fill((0, 0, 0))
            self.all_sprites.draw(self.screen)

            # Draw input sequence
            text = self.font.render("Sequence: " + " ".join(self.input_sequence), True, (255, 255, 255))
            self.screen.blit(text, (10, 10))

            pygame.display.flip()
            self.clock.tick(60)

# Function to generate a sine wave for a given frequency
def generate_tone(frequency, duration=0.1):
    # Calculate number of samples
    samples = int(SAMPLE_RATE * duration)
    # Generate x values
    x = np.arange(samples)
    # Calculate sine wave
    y = 32767 * 0.5 * np.sin(2 * np.pi * frequency * x / SAMPLE_RATE)
    # Convert to stereo by duplicating the mono channel
    stereo_wave = np.tile(y, (2, 1)).T.astype(np.int16)
    # Ensure contiguity in memory for pygame
    stereo_wave = np.ascontiguousarray(stereo_wave)
    # Return stereo wave
    return stereo_wave

if __name__ == "__main__":
    game = Game()
    game.run()
