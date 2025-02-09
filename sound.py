import pygame
import pygame.midi

from constants import *
from enum import Enum


class Note(Enum):
    A = "a"
    B = "b"
    C = "c"
    D = "d"
    E = "e"
    F = "f"
    G = "g"


# define all the constant values -----------------------------------------------
device = 0  # device number in win10 laptop
instrument = 9  # http://www.ccarh.org/courses/253/handout/gminstruments/
note_Do = 48  # http://www.electronics.dit.ie/staff/tscarff/Music_technology/midi/midi_note_numbers_for_octaves.htm
note_Re = 50
note_Me = 52
volume = 127
wait_time = 0.5


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
        self.player = pygame.midi.Output(0)

        # set the instrument -----------------------------------------------------------
        self.player.set_instrument(instrument)
        pygame.mixer.init(frequency=SAMPLE_RATE, size=-16, channels=2, buffer=512)
        self.note_sounds = {
            Note.C: 0,  # A4
            Note.D: 2,  # B4
            Note.E: 3,  # C5
            Note.G: 6,  # D5
            Note.A: 8,  # E5
        }

        self.midi_note_mapping = {
            Note.A: 0,  # A3
            Note.B: 1,  # B3
            Note.C: 2,  # C3
            Note.D: 3,  # D3
            Note.E: 4,  # E3
            Note.F: 5,  # F3
            Note.G: 6,  # G3
        }

    def play_note(self, note: Note):
        if note in self.midi_note_mapping:
            midi_note = self.midi_note_mapping[note]
            filename = (
                f"Piano{midi_note + 111}.ogg"  # filenames start from 111, and C3 is 48
            )
            try:
                sound = pygame.mixer.Sound(filename)
                sound.play(maxtime=300, fade_ms=10)
            except pygame.error as e:
                print(f"Error playing {filename}: {e}")

    def quit(self):
        del self.player
        pygame.midi.quit()

        # del device
        # octave = self.note_sounds[note] * 2
        # octave.play()
