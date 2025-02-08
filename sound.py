import pygame
import numpy as np
from constants import *

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

class SoundManager:
    def __init__(self):
        pygame.mixer.init(frequency=SAMPLE_RATE, size=-16, channels=2, buffer=512)
        self.note_sounds = {
            'a': self.generate_tone(440),   # A4
            'b': self.generate_tone(494),   # B4
            'c': self.generate_tone(523),   # C5
            'd': self.generate_tone(587),   # D5
            'e': self.generate_tone(659),   # E5
            'f': self.generate_tone(698),   # F5
            'g': self.generate_tone(784)    # G5
        }

    def generate_tone(self, frequency, duration=0.1):
        samples = int(SAMPLE_RATE * duration)
        # Create stereo sound buffer
        wave_data = np.tile(
            32767 * 0.5 * np.sin(2 * np.pi * frequency * np.arange(samples) / SAMPLE_RATE),
            (2, 1)
        ).T.astype(np.int16)
        wave_data = np.ascontiguousarray(wave_data)
        # Convert directly to pygame sound
        return pygame.sndarray.make_sound(wave_data)
    
    def play_note(self, note):
        if note in self.note_sounds:
            self.note_sounds[note].play()
