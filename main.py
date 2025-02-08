import pygame
import sys
import numpy as np
from entities.player import Player
from entities.platforms import Platform
from constants import *
from game import Game

if __name__ == "__main__":
    game = Game()
    game.run()
