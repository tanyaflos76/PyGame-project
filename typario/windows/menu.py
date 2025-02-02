from typing import TYPE_CHECKING

import pygame
from pygame.event import Event

from typario.components.button import Button
from typario.utils.image import load_image

from .abc import BaseScreen


if TYPE_CHECKING:
    from typario.game import Game


class MenuWindow(BaseScreen):
    def __init__(self, game: "Game"):
        super().__init__(game)
        self.background = pygame.transform.scale(load_image("background_1.jpg"), game.size)
        self.font = pygame.font.Font("data/font_1.otf", 230)
        self.btn_font = pygame.font.Font("data/font_2.ttf", 40)

        self.rus_lang = Button(game.screen, self.btn_font, 410, 370, 400, 80, "Русский язык")
        self.eng_lang = Button(game.screen, self.btn_font, 410, 480, 400, 80, "English language")
        self.buttons = [self.rus_lang, self.eng_lang]
        self.button_is_clicked = 0

    def handle_events(self, events: list[Event]) -> None:
        for event in events:
            if event.type == pygame.QUIT:
                pass
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.rus_lang.get_click(event.pos):
                    self.button_is_clicked = 1
                elif self.eng_lang.get_click(event.pos):
                    self.button_is_clicked = 2
            # FIX: hard-coded ....
            if self.button_is_clicked == 1:
                self.next_screen = ("difficulty", {"language": "russian"})
            elif self.button_is_clicked == 2:
                self.next_screen = ("difficulty", {"language": "english"})

    def update(self) -> None:
        return super().update()

    def render(self, surface: pygame.Surface) -> None:
        intro_text = ["Typario"]
        surface.blit(self.background, (0, 0))
        text_coord = 20
        for line in intro_text:
            string_rendered = self.font.render(line, 1, pygame.Color(148, 226, 213))
            intro_rect = string_rendered.get_rect()
            intro_rect.top = text_coord
            intro_rect.left = text_coord + 270
            surface.blit(string_rendered, intro_rect)
        for button in self.buttons:
            button.render()
        pygame.draw.rect(surface, '#cdd6f4', ((310, 300), (620, 330)), 2)

