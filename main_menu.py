import pygame

import constants

pygame.mixer.init()


class Button:
    def __init__(self, text, x, y, width, height, centre, box, func):
        self.text = text

        if centre:
            self.x = x - width // 2
            self.y = y - height // 2

        else:
            self.x = x
            self.y = y

        self.width = width
        self.height = height

        self.box = box

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.func = func

    def drawButton(self, screen):
        if self.box:
            pygame.draw.rect(screen, constants.GREEN, self.rect, 6, 2)
        text = constants.BIG_TEXT_FONT.render(str(self.text), 1, constants.BLACK)
        size = constants.BIG_TEXT_FONT.size(str(self.text))
        x = self.x + self.width // 2 - size[0] // 2
        y = self.y + self.height // 2 - size[1] // 2

        screen.blit(text, (x, y))


def makeMenu(game_instance):
    buttons = []
    txts = ["PLAY", "QUIT"]
    funcs = [lambda: (pygame.mixer.music.stop(), game_instance.run()), lambda: 0]
    buttons.append(
        Button(
            "Rogue Composer",
            constants.SCREEN_WIDTH // 2,
            100,
            300,
            150,
            True,
            False,
            lambda: 1,
        )
    )
    gap = constants.SCREEN_HEIGHT // (len(txts) + 2)
    for indx, (txt, func) in enumerate(zip(txts, funcs)):
        buttons.append(
            Button(
                txt,
                constants.SCREEN_WIDTH // 2,
                gap * (indx + 2),
                300,
                gap - 20,
                True,
                True,
                func,
            )
        )

    return buttons


def drawMenu(screen, background, buttons):
    # screen.fill(BLACK)

    # screen.blit(background, (0, 0))
    screen.blit(
        pygame.transform.scale(
            background, (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
        ),
        (0, 0),
    )
    for button in buttons:
        button.drawButton(screen)

    pygame.display.flip()


def menu(game_instance):
    buttons = makeMenu(game_instance)

    background = game_instance.BACKGROUND_IMAGE
    choice = -1

    # pygame.mixer.music.load("Rogue Composer Main Theme MIDI.mp3")
    pygame.mixer.music.load("output.mp3")

    pygame.mixer.music.play(-1)  # Play indefinitely

    while choice != 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                choice = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for button in buttons:
                    if button.rect.collidepoint(mouse_x, mouse_y):
                        choice = button.func()

        drawMenu(game_instance.screen, background, buttons)
    return 0


if __name__ == "__main__":
    menu(pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)))
