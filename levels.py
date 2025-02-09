from constants import *
import pygame

level_0_platforms = [
    {"x": 0, "y": SCREEN_HEIGHT - 40, "width": SCREEN_WIDTH, "height": 40}
]

level_1_platforms = [
    {"x": 0, "y": SCREEN_HEIGHT - 40, "width": SCREEN_WIDTH, "height": 40}
]
level_2_platforms = [
    {"x": 0, "y": SCREEN_HEIGHT - 40, "width": 3 * SCREEN_WIDTH / 5, "height": 40},
    {
        "x": 3 * SCREEN_WIDTH / 5,
        "y": SCREEN_HEIGHT - 100,
        "width": SCREEN_WIDTH / 5,
        "height": 40,
    },
    {
        "x": 4 * SCREEN_WIDTH / 5,
        "y": SCREEN_HEIGHT - 40,
        "width": SCREEN_WIDTH / 5,
        "height": 40,
    },
]

levels = [
    {
        "platforms": level_2_platforms,
        "enemies": [
            {
                "x": 350,
                "y": SCREEN_HEIGHT - 200,
                "width": 30,
                "height": 50,
                "color": "BLUE",
                "behavior": ["stab"],
                "platforms": level_0_platforms,
            }
        ],
        "apples": [{"x": SCREEN_WIDTH - 40, "y": SCREEN_HEIGHT - 80}],
    },
    {
        "platforms": level_0_platforms,
        "enemies": [
            {
                "x": 350,
                "y": SCREEN_HEIGHT - 200,
                "width": 30,
                "height": 50,
                "color": "BLUE",
                "behavior": ["stab"],
                "platforms": level_0_platforms,
            }
        ],
        "apples": [{"x": 600, "y": SCREEN_HEIGHT - 80}],
    },
    {
        "platforms": level_1_platforms,
        "enemies": [
            {
                "x": 450,
                "y": SCREEN_HEIGHT - 200,
                "width": 30,
                "height": 50,
                "color": "BLUE",
                "behavior": ["move_left"],
                "platforms": level_1_platforms,
            }
        ],
        "apples": [{"x": 600, "y": SCREEN_HEIGHT - 80}],
    },
    {
        "platforms": level_1_platforms,
        "enemies": [
            {
                "x": 450,
                "y": SCREEN_HEIGHT - 200,
                "width": 30,
                "height": 50,
                "color": "BLUE",
                "behavior": ["move_left", "move_right", "stab"],
                "platforms": level_1_platforms,
            }
        ],
        "apples": [{"x": 600, "y": SCREEN_HEIGHT - 80}],
    },
    {
        "platforms": level_1_platforms,
        "enemies": [
            {
                "x": 450,
                "y": SCREEN_HEIGHT - 200,
                "width": 30,
                "height": 50,
                "color": "BLUE",
                "behavior": ["move_left", "move_right", "stab"],
                "platforms": level_1_platforms,
            },
            {
                "x": 550,
                "y": SCREEN_HEIGHT - 200,
                "width": 30,
                "height": 50,
                "color": "BLUE",
                "behavior": ["stab", "move_right", "move_left"],
                "platforms": level_1_platforms,
            },
        ],
        "apples": [{"x": 600, "y": SCREEN_HEIGHT - 80}],
    },
]
