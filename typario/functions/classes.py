import pygame


class Button:
    def __init__(self, screen, font, x, y, width, height, button_text='Button'):
        self.x = x
        self.y = y
        self.screen = screen
        self.width = width
        self.height = height
        self.font = font

        self.fill_colors = {
            'normal': '#FFFFFF',
            'hover': '#587E89',
            'pressed': '#03202E',
        }

        self.button_surface = pygame.Surface((self.width, self.height))
        self.button_rect = pygame.Rect((self.x, self.y), (self.width, self.height))
        self.button_surf = self.font.render(button_text, True, (20, 20, 20))

    def process(self):
        mouse_pos = pygame.mouse.get_pos()
        self.button_surface.fill(self.fill_colors['normal'])
        if self.button_rect.collidepoint(mouse_pos):
            self.button_surface.fill(self.fill_colors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.button_surface.fill((0, 0, 0))
                self.screen.blit(self.button_surface, self.button_rect)

        self.button_surface.blit(self.button_surf, [
            self.button_rect.width / 2 - self.button_surf.get_rect().width / 2,
            self.button_rect.height / 2 - self.button_surf.get_rect().height / 2
        ])
        self.screen.blit(self.button_surface, self.button_rect)

    def get_click(self, pos):
        mouse_pos = pos
        if (mouse_pos[0] >= self.button_rect.left) and (mouse_pos[0] <= self.button_rect.right) and (
                (mouse_pos[1] >= self.button_rect.top) and (mouse_pos[1] <= self.button_rect.bottom)):
            self.process()
            return True
