import json
import random
import time


class Spawner:
    def __init__(self, filename: str) -> None:
        self.filename: str = filename
        self.word_list: list[str] = self._extract_words(self.filename)
        self.user_input: str = ""

        self.start_time: float = time.time()
        self._amount: int = 20

    def spawn_words(self) -> None:
        self.current_words = random.choices(self.word_list, k=self._amount)
        self.user_input = ""

    def handle_input(self, input: str):
        if self.user_input and input == "\b":  # backspace
            self.user_input = self.user_input[:-1]
        if input != "\b":
            self.user_input += input

    @property
    def green_indexes(self):
        words = " ".join(self.current_words)
        user_input = self.user_input[: min(len(self.user_input), len(words))]
        res = [i for i, (c1, c2) in enumerate(zip(user_input, words)) if c1 == c2]
        return res

    @property
    def red_indexes(self):
        words = " ".join(self.current_words)
        user_input = self.user_input[: min(len(self.user_input), len(words))]
        res = [i for i, (c1, c2) in enumerate(zip(user_input, words)) if c1 != c2]
        return res

    def _extract_words(self, filename: str) -> list[str]:
        """Takes JSON with `words: list[str]` attribute"""
        with open(filename, "r") as f:
            return json.load(f)["words"]
