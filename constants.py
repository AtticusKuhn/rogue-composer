from enum import Enum, auto
from typing import Tuple

# Display settings
SCREEN_SIZE: Tuple[int, int] = (800, 600)
FPS: int = 60
BG_COLOR: Tuple[int, int, int] = (0, 0, 0)
UI_FONT_SIZE: int = 36
UI_FONT_COLOR: Tuple[int, int, int] = (255, 255, 255)

# Physics
GRAVITY: float = 0.8
JUMP_POWER: float = -15
BIG_JUMP_POWER: float = -20
MOVE_SPEED: int = 5

# Platform
PLATFORM_COLOR: Tuple[int, int, int] = (100, 100, 100)
GROUND_HEIGHT: int = 40

# Audio
SAMPLE_RATE: int = 44100
SOUND_DURATION: float = 0.1

class Action(Enum):
    MOVE_RIGHT = auto()
    MOVE_LEFT = auto()
    JUMP = auto()
    BIG_JUMP = auto()
    
    @classmethod
    def from_key(cls, key: str) -> 'Action':
        return {
            'a': cls.MOVE_LEFT,
            'd': cls.MOVE_RIGHT,
            'c': cls.JUMP,
            'd': cls.BIG_JUMP
        }.get(key.lower())
