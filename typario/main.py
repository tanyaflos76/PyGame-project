import logging

import pygame

from typario.core.config import GameConfig


# TODO: implement Game class
def main() -> None:
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s   %(name)-25s %(levelname)-8s %(message)s",
    )

    config = GameConfig()

    pygame.init()

    SIZE = (1200, 700)

    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    running = False

        clock.tick(config.fps)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
