import pygame

from game import Game
import constants

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

class Button:
    def __init__(self, text, x, y, width, height, centre, func):
        self.text = text

        if centre:
            self.x = x - width // 2
            self.y = y - height // 2

        else:
            self.x = x
            self.y = y

        self.width = width
        self.height = height

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.func = func

    def drawButton(self, screen):
        pygame.draw.rect(screen, CYAN, self.rect, 6, 2)
        text = BIG_TEXT_FONT.render(str(self.text), 1, BLACK)
        size = BIG_TEXT_FONT.size(str(self.text))
        x = self.x + self.width // 2 - size[0] // 2
        y = self.y + self.height // 2 - size[1] // 2

        screen.blit(text, (x, y))


def makeMenu(game_instance):
    buttons = []
    txts = ["Rogue Composer", "PLAY", "QUIT"]
    funcs = [lambda _: 1, game_instance.run(), lambda _: 0]

    gap = constants.SCREEN_HEIGHT // (len(txts) + 1)
    for indx, (txt, func) in enumerate(zip(txts, funcs)):
        buttons.append(Button(txt, constants.SCREEN_WIDTH // 2, gap * (indx + 1),
                       400, gap - 10, True, func))

    return buttons


def drawMenu(screen, background, buttons):
    # screen.fill(BLACK)

    screen.blit(background, (0, 0))
    for button in buttons:
        button.drawButton(screen)

    pygame.display.flip()


def menu(game_instance):
    buttons = makeMenu()
    background = BACKGROUND_IMAGE
    choice = -1
    while choice != 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                choice = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for button in buttons:
                    if button.rect.collidepoint(mouse_x, mouse_y):
                        choice = button.func(game_instance.screen)

        drawMenu(game_instance.screen, background, buttons)
    return 0


if __name__ == "__main__":
    menu(pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)))
