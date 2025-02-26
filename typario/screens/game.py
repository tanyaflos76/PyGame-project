from typing import TYPE_CHECKING

import pygame
from pygame.event import Event

from typario.lib.spawner import Spawner
from typario.screens.abc import BaseScreen


if TYPE_CHECKING:
    from typario.game import Game


class GameScreen(BaseScreen):
    def __init__(self, game: "Game", word_list_file: str):
        super().__init__(game)
        self.word_list_file = word_list_file
        self.spawner = Spawner(self.word_list_file)
        self.spawner.spawn_words()

        self.font = pygame.font.Font("data/font_3.ttf", 30)
        self.text_rect = pygame.Rect(20, 400, 1250, 400)
        self.score_rect = pygame.Rect(20, 20, 200, 40)
        self.hp_rect = pygame.Rect(20, 60, 200, 20)

    def handle_events(self, events: list[Event]) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key and event.key == pygame.K_ESCAPE:
                    self.game_over()
                elif event.unicode:
                    self.spawner.handle_input(event.unicode)

    def update(self):
        self.spawner.update_hp()
        if self.spawner.hp <= 0:
            self.game_over()

    def render(self, surface: pygame.Surface):
        surface.fill((30, 30, 46))

        words = " ".join(self.spawner.current_words)
        red, green, passed = self.spawner.red_indexes, self.spawner.green_indexes, self.spawner.passed_indexes
        # Drawing words
        self.draw_text(
            surface,
            words,
            (255, 255, 255),
            self.text_rect,
            self.font,
            red_indexes=red,
            green_indexes=green,
            passed_indexes=passed,
        )
        # Drawing score
        self.draw_text(
            surface,
            f"Score: {self.spawner.score}",
            (203, 166, 247),
            self.score_rect,
            self.font,
        )
        self.draw_hp_bar(surface)

    def game_over(self):
        self.next_screen = ("game_over", {"language": self.word_list_file, "score": self.spawner.score})

    def draw_hp_bar(self, surface: pygame.Surface):
        max_hp = 100
        current_hp = self.spawner.hp

        hp_width = int((current_hp / max_hp) * self.hp_rect.width)
        pygame.draw.rect(surface, (243, 139, 168), self.hp_rect)  # Красный фон
        pygame.draw.rect(
            surface, (166, 227, 161), (self.hp_rect.x, self.hp_rect.y, hp_width, self.hp_rect.height)
        )  # зеленый

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
        passed_indexes: list[int] = [],
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

                word_index = 0
                current_length = 0
                for word in self.spawner.current_words:
                    if current_length <= letter_index < current_length + len(word):
                        break
                    current_length += len(word) + 1  # +1 для пробела
                    word_index += 1

                if letter_index in green_indexes:
                    image = image.convert_alpha()
                    image.fill((166, 227, 161), special_flags=pygame.BLEND_RGBA_MULT)
                elif letter_index in red_indexes:
                    image = image.convert_alpha()
                    image.fill((243, 139, 168), special_flags=pygame.BLEND_RGBA_MULT)

                if word_index in passed_indexes:
                    image = image.convert_alpha()
                    image.fill((127, 132, 156), special_flags=pygame.BLEND_RGBA_MULT)

                surface.blit(image, (round(x), y))
                lineLeft += image.get_width()
            lineBottom += fontHeight + lineSpacing

        if lastLine < len(lineList):
            drawLetters = sum([len(lineList[i]) for i in range(lastLine)])
            remainingText = "".join(listOfLetters[drawLetters:])
            return remainingText
        return ""
