import pygame
import sys
from entities.player import Player
from entities.platforms import Platform
from sound import SoundManager, Note, toNote
from constants import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Synesthesia")
        self.clock = pygame.time.Clock()
        self.all_sprites: pygame.sprite.Group = pygame.sprite.Group()
        self.platforms: pygame.sprite.Group = pygame.sprite.Group()
        self.font = pygame.font.Font(None, 36)
        self.cursor: int = -1
        # Note positions (mapping notes to vertical positions)
        self.note_positions: dict[Note, int] = {
            Note.A: SCREEN_HEIGHT - 100,
            Note.B: SCREEN_HEIGHT - 120,
            Note.C: SCREEN_HEIGHT - 140,
            Note.D: SCREEN_HEIGHT - 160,
            Note.E: SCREEN_HEIGHT - 180,  # Corrected typo
            Note.F: SCREEN_HEIGHT - 200,
            Note.G: SCREEN_HEIGHT - 220,
        }

        self.sound_manager: SoundManager = SoundManager()

        # Create ground platform
        self.platforms.add(Platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40))
        self.player: Player = Player()
        self.all_sprites.add(self.player, *self.platforms)

        self.input_sequence: list[Note] = []
        self.playing_sequence: bool = False

    def _handle_events(self):
        """Handle user input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if not self.playing_sequence:
                    if event.unicode in "abcdefg":
                        note: Note = toNote(event.unicode)
                        self.input_sequence.append(note)
                        self.sound_manager.play_note(note)
                    elif event.key == pygame.K_SPACE:
                        self.playing_sequence = True
                        self.execute_sequence()

            if event.type == pygame.USEREVENT:
                self.execute_sequence()

    def execute_sequence(self) -> None:
        """Executes the current note sequence."""
        # if self.input_sequence:
        if self.cursor < len(self.input_sequence) - 1:
            self.cursor += 1
            current_note: Note = self.input_sequence[self.cursor]
            self.player.handle_note(current_note)
            self.sound_manager.play_note(current_note)

            # Queue next action
            if self.input_sequence:
                pygame.time.set_timer(pygame.USEREVENT, 500)
            else:
                pygame.time.set_timer(pygame.USEREVENT, 0)
                self.playing_sequence = False

    def draw_note(self, note: Note, position: int, cursor: int) -> None:
        """Draws a note on the screen."""
        x: int = 10 + position * 60  # Horizontal spacing
        y: int = (
            self.note_positions.get(note, SCREEN_HEIGHT - 100) - 50
        )  # Default to 'a' position
        color: tuple[int, int, int] = (
            (0, 255, 0)
            if cursor == position
            else (255, 255, 255) if cursor < position else (128, 128, 128)
        )
        pygame.draw.rect(self.screen, color, (x, y, 40, 20))

    def run(self) -> None:
        """Main game loop."""
        while True:
            self._handle_events()
            self.player.update(self.platforms)

            self.screen.fill((0, 0, 0))
            self.all_sprites.draw(self.screen)

            # Draw input sequence
            for i, note in enumerate(self.input_sequence):
                self.draw_note(note, i, self.cursor)

            pygame.display.flip()
            self.clock.tick(30)
