import logging

import pygame

from typario.components.button import Button
from typario.core.config import GameConfig
from typario.utils.image import load_image


class Difficulty:
    def __init__(self, language, width, height):
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s   %(name)-25s %(levelname)-8s %(message)s",
        )

        self.size = (width, height)
        screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.config = GameConfig()
        self.buttons = []
        self.language = language

        text = {
            "english": [["Difficulty level"], "easy", "normal", "hard"],
            "русский": [["Уровень сложности"], "легкий", "средний", "трудный"],
        }

        background = pygame.transform.scale(load_image("background_1.jpg"), self.size)
        screen.blit(background, (0, 0))
        font = pygame.font.Font("data/font_1.otf", 120)
        text_coord = 60
        for line in text[self.language][0]:
            string_rendered = font.render(line, 1, pygame.Color(255, 255, 255))
            text_rect = string_rendered.get_rect()
            text_rect.top = text_coord
            if language == "русский":
                text_rect.x = 140
            else:
                text_rect.x = 280
            text_coord += text_rect.height
            screen.blit(string_rendered, text_rect)

        self.button1 = Button(screen, pygame.font.Font("data/font_2.ttf", 40), 390, 280, 400, 80, text[language][1])
        self.button2 = Button(screen, pygame.font.Font("data/font_2.ttf", 40), 390, 410, 400, 80, text[language][2])
        self.button3 = Button(screen, pygame.font.Font("data/font_2.ttf", 40), 390, 540, 400, 80, text[language][3])
        pygame.draw.rect(screen, (255, 255, 255), ((290, 250), (600, 400)), 2)
        self.buttons.append(self.button1)
        self.buttons.append(self.button2)
        self.buttons.append(self.button3)
        self.difficulty_level = 0

    def start(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pass
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.button1.get_click(event.pos):
                        self.difficulty_level = 1
                    if self.button2.get_click(event.pos):
                        self.difficulty_level = 2
                    if self.button3.get_click(event.pos):
                        self.difficulty_level = 3
                for button in self.buttons:
                    button.process()
                    if self.difficulty_level:
                        return self.difficulty_level
            pygame.display.flip()
            self.clock.tick(self.config.fps)
