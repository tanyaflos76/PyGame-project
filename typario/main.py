import pygame

from functions.launch_window import Menu
from functions.difficulty_window import Difficulty

languages = ['русский', 'english']

# TODO: implement Game class


if __name__ == "__main__":
    pygame.init()
    menu = Menu(1200, 700)
    language = languages[menu.start() - 1]
    difficulty = Difficulty(language, 1200, 700)
    level = difficulty.start()
