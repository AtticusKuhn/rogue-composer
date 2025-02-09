# Game constants
import pygame
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRAVITY = 0.8
JUMP_POWER = -15
BIG_JUMP_POWER = -20
MOVE_SPEED = 5
SAMPLE_RATE = 44100
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
LIME_GREEN = (30, 255, 70)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREY = (127, 127, 127)
PINK = (230, 120, 120)
CYAN = (5, 255, 255)
ORANGE = (255, 165, 0)

BIG_TEXT_SIZE = 48
BIG_TEXT_FONT = pygame.font.SysFont("futura", BIG_TEXT_SIZE)

BACKGROUND_IMAGE = pygame.image.load("background_image.png").convert()