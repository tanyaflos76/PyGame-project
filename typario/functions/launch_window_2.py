import logging

import pygame

from typario.core.config import GameConfig
from typario.functions.classes import Button
from typario.functions.utils import load_image, terminate


def choice_level(language):
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

    text = {'english': [['Difficulty level'], 'easy', 'normal', 'hard'],
            'русский': [['Уровень сложности'], 'легкий', 'средний', 'трудный']}

    background = pygame.transform.scale(load_image("background_1.jpg"), (WIDTH, HEIGHT))
    screen.blit(background, (0, 0))
    font = pygame.font.Font("data/font_1.otf", 120)
    text_coord = 60
    for line in text[language][0]:
        string_rendered = font.render(line, 1, pygame.Color(255, 255, 255))
        text_rect = string_rendered.get_rect()
        text_rect.top = text_coord
        if language == 'русский':
            text_rect.x = 140
        else:
            text_rect.x = 290
        text_coord += text_rect.height
        screen.blit(string_rendered, text_rect)

    button1 = Button(screen, pygame.font.Font('data/font_2.ttf', 40), 390, 280, 400, 80, text[language][1])
    button2 = Button(screen, pygame.font.Font('data/font_2.ttf', 40), 390, 410, 400, 80, text[language][2])
    button3 = Button(screen, pygame.font.Font('data/font_2.ttf', 40), 390, 540, 400, 80, text[language][3])
    pygame.draw.rect(screen, (255, 255, 255), ((290, 250), (600, 400)), 2)
    buttons.append(button1)
    buttons.append(button2)
    buttons.append(button3)
    difficulty_level = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button1.get_click(event.pos):
                    difficulty_level = 1
                if button2.get_click(event.pos):
                    difficulty_level = 2
                if button3.get_click(event.pos):
                    difficulty_level = 3
            for button in buttons:
                button.process()
                if difficulty_level:
                    return difficulty_level
        pygame.display.flip()
        clock.tick(config.fps)
