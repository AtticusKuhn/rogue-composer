import pygame
import numpy as np
from constants import *
from enum import Enum
import time





class Note(Enum):
    A = "a"
    B = "b"
    C = "c"
    D = "d"
    E = "e"
    F = "f"
    G = "g"


def toNote(note: str) -> Note:
    if note == "a":
        return Note.A
    elif note == "b":
        return Note.B
    elif note == "c":
        return Note.C
    elif note == "d":
        return Note.D
    elif note == "e":
        return Note.E
    elif note == "f":
        return Note.F
    elif note == "g":
        return Note.G


class SoundManager:
    def __init__(self):
        pygame.midi.init()
        pygame.mixer.init(frequency=SAMPLE_RATE, size=-16, channels=2, buffer=512)
        self.note_sounds = {
            Note.C: 0,  # A4
            Note.D: 2,  # B4
            Note.E: 3,  # C5
            Note.G: 6,  # D5
            Note.A: 8,  # E5
        }

    def play_note(self, note: Note):
        if note in self.note_sounds:
            player = pygame.midi.Output(self.note_sounds[note])
            player.set_instrument(0)
            player.note_on(64, 127)
            time.sleep(0.1)
            player.note_off(64, 127)
            del player
            # octave = self.note_sounds[note] * 2
            # octave.play()
