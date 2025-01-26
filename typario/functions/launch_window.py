import logging

import pygame
from typario.core.config import GameConfig
from typario.functions.classes import Button
from typario.functions.utils import load_image, terminate


class Menu:
    def __init__(self, width, height):
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s   %(name)-25s %(levelname)-8s %(message)s",
        )

        self.size = (width, height)
        screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.config = GameConfig()
        self.buttons = []

        intro_text = ["Typario"]

        background = pygame.transform.scale(load_image("background_1.jpg"), self.size)
        screen.blit(background, (0, 0))
        font = pygame.font.Font("data/font_1.otf", 230)
        text_coord = 20
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color(255, 255, 255))
            intro_rect = string_rendered.get_rect()
            intro_rect.top = text_coord
            intro_rect.left = text_coord + 260
            screen.blit(string_rendered, intro_rect)

        self.button1 = Button(screen, pygame.font.Font('data/font_2.ttf', 40), 390, 370, 400, 80, 'Русский язык')
        self.button2 = Button(screen, pygame.font.Font('data/font_2.ttf', 40), 390, 480, 400, 80, 'English language')
        pygame.draw.rect(screen, (255, 255, 255), ((290, 315), (600, 305)), 2)
        self.buttons.append(self.button1)
        self.buttons.append(self.button2)
        self.button_is_clicked = 0
    def start(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.button1.get_click(event.pos):
                        self.button_is_clicked = 1
                    if self.button2.get_click(event.pos):
                        self.button_is_clicked = 2
                for button in self.buttons:
                    button.process()
                    if self.button_is_clicked:
                        return self.button_is_clicked
            pygame.display.flip()
            self.clock.tick(self.config.fps)
