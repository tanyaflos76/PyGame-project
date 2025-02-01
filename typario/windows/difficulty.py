from typing import TYPE_CHECKING

import pygame
from pygame.event import Event

from typario.components.button import Button
from typario.utils.image import load_image
from typario.windows.abc import BaseScreen


if TYPE_CHECKING:
    from typario.game import Game


class DifficultyWindow(BaseScreen):
    def __init__(self, game: "Game", language: str):
        self.background = pygame.transform.scale(load_image("background_1.jpg"), game.size)
        self.font = pygame.font.Font("data/font_1.otf", 120)
        self.btn_font = pygame.font.Font("data/font_2.ttf", 40)

        self.language = language

        self.options = {
            "english": [["Difficulty level"], "easy", "normal", "hard"],
            "russian": [["Уровень сложности"], "легкий", "средний", "трудный"],
        }

        self.easy = Button(game.screen, self.btn_font, 390, 280, 400, 80, self.options[self.language][1])
        self.normal = Button(game.screen, self.btn_font, 390, 410, 400, 80, self.options[self.language][2])
        self.hard = Button(game.screen, self.btn_font, 390, 540, 400, 80, self.options[self.language][3])
        self.buttons = [self.easy, self.normal, self.hard]
        self.difficulty_level: int = 0

    def handle_events(self, events: list[Event]) -> None:
        for event in events:
            if event.type == pygame.QUIT:
                pass
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.easy.get_click(event.pos):
                    self.difficulty_level = 1
                elif self.normal.get_click(event.pos):
                    self.difficulty_level = 2
                elif self.hard.get_click(event.pos):
                    self.difficulty_level = 3

            match self.difficulty_level:
                case 1:
                    self.next_screen = ("game", {"word_list_file": f"{self.language}"})
                case 2:
                    self.next_screen = ("game", {"word_list_file": f"{self.language}_1k"})
                case 3:
                    self.next_screen = ("game", {"word_list_file": f"{self.language}_10k"})

    def update(self) -> None:
        return super().update()

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(self.background, (0, 0))
        text_coord = 60
        for line in self.options[self.language][0]:
            string_rendered = self.font.render(line, 1, pygame.Color(255, 255, 255))
            text_rect = string_rendered.get_rect()
            text_rect.top = text_coord
            if self.language == "russian":
                text_rect.x = 140
            else:
                text_rect.x = 280
            text_coord += text_rect.height
            surface.blit(string_rendered, text_rect)
        for button in self.buttons:
            button.render()

        pygame.draw.rect(surface, (255, 255, 255), ((290, 250), (600, 400)), 2)
