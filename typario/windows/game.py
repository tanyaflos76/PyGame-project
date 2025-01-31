import logging
from typing import TYPE_CHECKING

import pygame
from pygame.event import Event

from typario.lib.spawner import Spawner
from typario.windows.abc import BaseScreen


if TYPE_CHECKING:
    from typario.game import Game


class GameWindow(BaseScreen):
    def __init__(self, game: "Game", word_list_file: str):
        super().__init__(game)
        self.spawner = Spawner(word_list_file)
        self.spawner.spawn_words()

        self.font = pygame.font.Font(None, 36)
        self.text_rect = pygame.Rect(20, 400, 1250, 400)

    def render(self, surface: pygame.Surface):
        surface.fill((100, 100, 100))
        words = " ".join(self.spawner.current_words)
        red, green = self.spawner.red_indexes, self.spawner.green_indexes
        self.draw_text(
            surface,
            words,
            (255, 255, 255),
            self.text_rect,
            self.font,
            red_indexes=red,
            green_indexes=green,
        )

    def handle_events(self, events: list[Event]) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key and event.key == pygame.K_ESCAPE:
                    self.next_screen = ("menu",)
                elif event.unicode:
                    self.spawner.handle_input(event.unicode)

    def draw_text(
        self,
        surface: pygame.Surface,
        text: str,
        color: tuple[int, int, int],
        rect: pygame.Rect,
        font: pygame.font.Font,
        aa: bool = False,
        bkg: tuple[int, int, int] | None = None,
        green_indexes: list[int] = [],
        red_indexes: list[int] = [],
    ):
        lineSpacing = -2
        spaceWidth, fontHeight = font.size("")[0], font.size("Tg")[1]

        listOfLetters = list(text)
        if bkg:
            imageList = [font.render(letter, 1, color, bkg) for letter in listOfLetters]
            for image in imageList:
                image.set_colorkey(bkg)
        else:
            imageList = [font.render(letter, aa, color) for letter in listOfLetters]

        maxLen = rect[2]
        lineLenList = [0]
        lineList: list[list[pygame.Surface]] = [[]]
        for image in imageList:
            width = image.get_width()
            lineLen = lineLenList[-1] + len(lineList[-1]) * spaceWidth + width
            if len(lineList[-1]) == 0 or lineLen <= maxLen:
                lineLenList[-1] += width
                lineList[-1].append(image)
            else:
                lineLenList.append(width)
                lineList.append([image])

        lineBottom = rect[1]
        lastLine = 0
        for lineLen, lineImages in zip(lineLenList, lineList):
            lineLeft = rect[0]
            lineLeft += (rect[2] - lineLen - spaceWidth * (len(lineImages) - 1)) // 2
            if lineBottom + fontHeight > rect[1] + rect[3]:
                break
            lastLine += 1
            for i, image in enumerate(lineImages):
                x, y = lineLeft + i * spaceWidth, lineBottom

                letter_index = sum([len(lineList[j]) for j in range(lastLine - 1)]) + i
                if letter_index in green_indexes:
                    image = image.convert_alpha()
                    image.fill((0, 255, 0), special_flags=pygame.BLEND_RGBA_MULT)
                elif letter_index in red_indexes:
                    image = image.convert_alpha()
                    image.fill((255, 0, 0), special_flags=pygame.BLEND_RGBA_MULT)

                surface.blit(image, (round(x), y))
                lineLeft += image.get_width()
            lineBottom += fontHeight + lineSpacing

        if lastLine < len(lineList):
            drawLetters = sum([len(lineList[i]) for i in range(lastLine)])
            remainingText = "".join(listOfLetters[drawLetters:])
            return remainingText
        return ""
