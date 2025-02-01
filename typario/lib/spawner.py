import json
import logging
import random
import time


logger = logging.getLogger(__name__)


# FIX: класс-бог, ето плохо
class Spawner:
    def __init__(self, filename: str) -> None:
        self.filename: str = filename
        self.word_list: list[str] = self._extract_words(self.filename)
        self.user_words: list[str] = []

        self.start_time: float = time.time()
        self.score: int = 0
        self.hp: int = 100
        self._amount: int = 20
        self.last_update_time: float = time.time()

        self._points_for_word: int = 10
        self._hp_for_word: int = 10
        self._latency: float = 0.1

    def spawn_words(self) -> None:
        self.current_words = random.choices(self.word_list, k=self._amount)
        self.user_words.clear()

    def handle_input(self, input: str):
        if input == "\b":  # Обработка backspace
            if self.user_words:
                last_word = self.user_words[-1]
                if last_word:
                    self.user_words[-1] = last_word[:-1]
                else:
                    self.user_words.pop()
        elif input == " ":
            if len(self.user_words) >= 1 and self.user_words[-1] != "":
                self.user_words.append("")
        else:
            if not self.user_words:
                self.user_words.append("")
            self.user_words[-1] += input

        logger.debug("user_words=%s", self.user_words)

        self._update_score()
        self._check_for_input()

    def _check_for_input(self) -> None:
        if len(self.user_words) == len(self.current_words) and len(self.user_words[-1]) == len(self.current_words[-1]):
            self.spawn_words()

    def _update_score(self):
        last_word_idx = len(self.user_words) - 1
        if last_word_idx < 0 or last_word_idx >= len(self.current_words):
            return  # Если нет введенных слов, выходим

        user_word = self.user_words[last_word_idx]
        target_word = self.current_words[last_word_idx]

        if user_word == target_word:
            self.score += self._points_for_word
            self.hp = min(100, self.hp + self._hp_for_word)
        else:
            incorrect = sum(1 for c1, c2 in zip(user_word, target_word) if c1 != c2)
            self.score = max(0, self.score - incorrect)
            self.hp = max(0, self.hp - incorrect)

    def update_hp(self):
        current_time = time.time()
        if current_time - self.last_update_time >= self._latency:  # Уменьшаем HP каждую секунду
            self.hp = max(0, self.hp - 1)
            self.last_update_time = current_time

    @property
    def green_indexes(self):
        green = []
        current_pos = 0
        for user_word, target_word in zip(self.user_words, self.current_words):
            for i, (c1, c2) in enumerate(zip(user_word, target_word)):
                if c1 == c2:
                    green.append(current_pos + i)
            current_pos += len(target_word) + 1  # +1 для пробела между словами
        return green

    @property
    def red_indexes(self):
        red = []
        current_pos = 0
        for user_word, target_word in zip(self.user_words, self.current_words):
            for i, (c1, c2) in enumerate(zip(user_word, target_word)):
                if c1 != c2:
                    red.append(current_pos + i)
            current_pos += len(target_word) + 1  # +1 для пробела между словами
        return red

    @property
    def passed_indexes(self):
        _len = len(self.user_words) - 1
        user_idx = _len if _len else 0  # Like 3
        return [i for i in range(user_idx)]  # [0,1,2]

    def _extract_words(self, filename: str) -> list[str]:
        """Takes JSON with `words: list[str]` attribute"""
        filepath = f"data/languages/{filename}.json"
        with open(filepath, "r", encoding="utf8") as f:
            return json.load(f)["words"]
