import pygame
from typario.functions.utils import load_image, terminate

pygame.init()
size = WIDTH, HEIGHT = 1200, 700
screen = pygame.display.set_mode(size)
FPS = 60
clock = pygame.time.Clock()


def start_screen():
    intro_text = ["Typario"]

    background = pygame.transform.scale(load_image("background_1.jpg"),
                                        (WIDTH, HEIGHT))
    screen.blit(background, (0, 0))
    font = pygame.font.Font('data/Andy_Bold_0.otf', 230)
    text_coord = 20
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color(255, 255, 255))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = text_coord
        intro_rect.left = text_coord + 260
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


start_screen()
