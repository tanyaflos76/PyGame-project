import logging

import pygame

from typario.components.button import Button
from typario.core.config import GameConfig
from typario.functions.utils import load_image, terminate


def start_screen():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s   %(name)-25s %(levelname)-8s %(message)s",
    )

    pygame.init()
    size = WIDTH, HEIGHT = 1200, 700
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    config = GameConfig()
    buttons = []

    intro_text = ["Typario"]

    background = pygame.transform.scale(load_image("background_1.jpg"), (WIDTH, HEIGHT))
    screen.blit(background, (0, 0))
    font = pygame.font.Font("data/font_1.otf", 230)
    text_coord = 20
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color(255, 255, 255))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = text_coord
        intro_rect.left = text_coord + 260
        screen.blit(string_rendered, intro_rect)

    button1 = Button(screen, pygame.font.Font("data/font_2.ttf", 40), 390, 370, 400, 80, "Русский язык")
    button2 = Button(screen, pygame.font.Font("data/font_2.ttf", 40), 390, 480, 400, 80, "English language")
    pygame.draw.rect(screen, (255, 255, 255), ((290, 315), (600, 305)), 2)
    buttons.append(button1)
    buttons.append(button2)
    button_is_clicked = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button1.get_click(event.pos):
                    button_is_clicked = 1
                if button2.get_click(event.pos):
                    button_is_clicked = 2
            for button in buttons:
                button.process()
                if button_is_clicked:
                    terminate()
        pygame.display.flip()
        clock.tick(config.fps)
