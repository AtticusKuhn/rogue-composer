import pygame
import sys
import math
import numpy as np

# Initialize PyGame
pygame.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRAVITY = 0.8
JUMP_POWER = -15
BIG_JUMP_POWER = -20
MOVE_SPEED = 5

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 50))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(center=(100, SCREEN_HEIGHT//2))
        self.velocity = 0
        self.on_ground = False
        self.current_action = None  # Initialize action attribute

    def update(self, platforms):
        # Horizontal movement
        if hasattr(self, 'current_action'):
            if self.current_action == 'a':
                self.rect.x += MOVE_SPEED
            elif self.current_action == 'b':
                self.rect.x -= MOVE_SPEED
        
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

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill((100, 100, 100))
        self.rect = self.image.get_rect(topleft=(x, y))

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.font = pygame.font.Font(None, 36)
        
        # Initialize sound system with stereo output
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        self.note_sounds = {
            'a': self.generate_tone(440),   # A4
            'b': self.generate_tone(494),   # B4
            'c': self.generate_tone(523),   # C5
            'd': self.generate_tone(587),   # D5
            'e': self.generate_tone(659),   # E5
            'f': self.generate_tone(698),   # F5
            'g': self.generate_tone(784)    # G5
        }

        # Create ground platform
        self.platforms.add(Platform(0, SCREEN_HEIGHT-40, SCREEN_WIDTH, 40))
        self.player = Player()
        self.all_sprites.add(self.player, *self.platforms)
        
        self.input_sequence = []
        self.playing_sequence = False

    def generate_tone(self, frequency, duration=0.1):
        sample_rate = 44100
        samples = int(sample_rate * duration)
        # Create stereo sound buffer
        wave_data = np.tile(
            32767 * 0.5 * np.sin(2 * np.pi * frequency * np.arange(samples) / sample_rate),
            (2, 1)
        ).T.astype(np.int16)
        wave_data = np.ascontiguousarray(wave_data)
        # Convert directly to pygame sound
        return pygame.sndarray.make_sound(wave_data)

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
            self.note_sounds[current_note].play()  # Play corresponding sound
            
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

    def run(self):
        while True:
            self.handle_events()
            self.player.update(self.platforms)
            
            self.screen.fill((0, 0, 0))
            self.all_sprites.draw(self.screen)
            
            # Draw input sequence using music symbols
            text = self.font.render("Sequence: " + " ".join(self.input_sequence), True, (255, 255, 255))
            self.screen.blit(text, (10, 10))
            
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()
