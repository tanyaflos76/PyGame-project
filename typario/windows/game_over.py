from typing import TYPE_CHECKING

import pygame
from pygame.event import Event

from typario.components.button import Button
from typario.utils.image import load_image

from ..utils.records import add_value, find_record
from .abc import BaseScreen


if TYPE_CHECKING:
    from typario.game import Game


class GameOverScreen(BaseScreen):
    def __init__(self, game: "Game", language: str, score: int):
        super().__init__(game)
        self.background = pygame.transform.scale(load_image("background_1.jpg"), game.size)
        self.font = pygame.font.Font("data/font_1.otf", 150)
        self.font_score = pygame.font.Font("data/font_1.otf", 70)
        self.btn_font = pygame.font.Font("data/font_2.ttf", 40)
        self.language_main = language
        if "english" in self.language_main:
            self.language = "english"
        elif "russian" in self.language_main:
            self.language = "russian"
        add_value(score)
        self.record = find_record()

        self.options = {
            "russian": [["Игра окончена", f"Ваш рекорд: {self.record}"], "обратно в меню", "повторить", "выйти"],
            "english": [["Game over", f"Your record: {self.record}"], "back to menu", "retry", "exit"],
        }
        self.to_menu = Button(game.screen, self.btn_font, 410, 360, 400, 80, self.options[self.language][1])
        self.retry = Button(game.screen, self.btn_font, 410, 460, 400, 80, self.options[self.language][2])
        self.exit = Button(game.screen, self.btn_font, 410, 560, 400, 80, self.options[self.language][3])
        self.buttons = [self.retry, self.to_menu, self.exit]
        self.button_is_clicked = 0

    def handle_events(self, events: list[Event]) -> None:
        for event in events:
            if event.type == pygame.QUIT:
                pass
            elif event.type == pygame.KEYDOWN:
                if event.key and event.key == pygame.K_ESCAPE:
                    self.next_screen = ("menu",)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.retry.get_click(event.pos):
                    self.button_is_clicked = 1
                elif self.to_menu.get_click(event.pos):
                    self.button_is_clicked = 2
                elif self.exit.get_click(event.pos):
                    self.button_is_clicked = 3
            # FIX: hard-coded ....
            if self.button_is_clicked == 2:
                self.next_screen = ("menu",)
            elif self.button_is_clicked == 1:
                self.next_screen = ("game", {"word_list_file": f"{self.language_main}"})
            elif self.button_is_clicked == 3:
                self.next_screen = ("exit",)

    def update(self) -> None:
        return super().update()

    def render(self, surface: pygame.Surface) -> None:
        text = self.options[self.language][0]
        surface.blit(self.background, (0, 0))
        text_coord = 20
        for i, line in enumerate(text):
            if i == 1:
                string_rendered = self.font_score.render(line, 1, pygame.Color(148, 226, 213))
            else:
                string_rendered = self.font.render(line, 1, pygame.Color(148, 226, 213))
            text_rect = string_rendered.get_rect()
            text_rect.top = text_coord
            if self.language == "russian":
                text_rect.x = 205
            else:
                text_rect.x = 310
            if i == 1 and self.language == "russian":
                text_rect.x += 175
                text_rect.y += 30
            elif i == 1 and self.language == "english":
                text_rect.x += 80
                text_rect.y += 30
            text_coord += text_rect.height
            surface.blit(string_rendered, text_rect)
        for button in self.buttons:
            button.render()
        pygame.draw.rect(surface, "#cdd6f4", ((310, 330), (610, 340)), 2)
