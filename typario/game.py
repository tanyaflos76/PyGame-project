import logging
from typing import Any

import pygame

from typario.core.config import GameConfig
from typario.windows import GameWindow
from typario.windows.abc import BaseScreen
from typario.windows.difficulty import DifficultyWindow
from typario.windows.game_over import GameOverScreen
from typario.windows.menu import MenuWindow


class Game:
    def __init__(self):
        pygame.init()

        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s   %(name)-25s %(levelname)-8s %(message)s",
        )

        self.config = GameConfig()

        self.size = 1280, 720
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.running = True

        self.current_screen: BaseScreen | None = None
        self.screens: dict[str, type[BaseScreen]] = {
            "menu": MenuWindow,
            "difficulty": DifficultyWindow,
            "game": GameWindow,
            "game_over": GameOverScreen,
        }

    def switch_screen(self, screen_name: str, **kwargs: Any):
        screen_class = self.screens.get(screen_name, None)
        if screen_class:
            self.current_screen = screen_class(self, **kwargs)

    def run(self):
        self.switch_screen("menu")  # Initial screen
        assert self.current_screen

        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            self.current_screen.handle_events(events)

            if self.current_screen.next_screen:
                next_name, *next_args = self.current_screen.next_screen
                self.switch_screen(next_name, **next_args[0] if next_args else {})
                self.current_screen.next_screen = None

            self.screen.fill((0, 0, 0))
            self.current_screen.update()
            self.current_screen.render(self.screen)
            pygame.display.flip()
            self.clock.tick(self.config.fps)
