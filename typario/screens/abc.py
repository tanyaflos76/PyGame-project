from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

import pygame
from pygame.event import Event


if TYPE_CHECKING:
    from typario.game import Game


class BaseScreen(ABC):
    def __init__(self, game: "Game", **kwargs: Any):
        self.game = game
        self.next_screen: tuple[str, dict[str, Any]] | tuple[str] | None = None
        self.kwargs = kwargs

    @abstractmethod
    def handle_events(self, events: list[Event]) -> None:
        pass

    @abstractmethod
    def update(self) -> None:
        pass

    @abstractmethod
    def render(self, surface: pygame.Surface) -> None:
        pass
