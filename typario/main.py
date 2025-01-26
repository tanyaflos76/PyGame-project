from functions.launch_window import start_screen
from functions.launch_window_2 import choice_level

language = ['русский', 'english']

# TODO: implement Game class


if __name__ == "__main__":
    language = language[start_screen() - 1]
    level = choice_level(language)
