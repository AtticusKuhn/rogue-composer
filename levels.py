from constants import *
import pygame

level_0_platforms = [
    {"x": 0, "y": SCREEN_HEIGHT - 40, "width": SCREEN_WIDTH, "height": 40}
]

level_1_platforms = [
    {"x": 0, "y": SCREEN_HEIGHT - 40, "width": SCREEN_WIDTH, "height": 40}
]

levels = [
    # {
    #     "platforms": level_0_platforms,
    #     "enemies": [
    #         {
    #             "x": 350,
    #             "y": SCREEN_HEIGHT - 200,
    #             "width": 30,
    #             "height": 50,
    #             "color": "BLUE",
    #             "behavior": ["stab"],
    #             "platforms": level_0_platforms,
    #         }
    #     ],
    #     "apples": [{"x": 600, "y": SCREEN_HEIGHT - 80}],
    # },
    # {
    #     "platforms": level_1_platforms,
    #     "enemies": [
    #         {
    #             "x": 450,
    #             "y": SCREEN_HEIGHT - 200,
    #             "width": 30,
    #             "height": 50,
    #             "color": "BLUE",
    #             "behavior": ["move_left"],
    #             "platforms": level_1_platforms,
    #         }
    #     ],
    #     "apples": [{"x": 600, "y": SCREEN_HEIGHT - 80}],
    # },
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
]
