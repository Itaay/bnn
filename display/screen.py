import pygame
from skeleton.node import Node

pygame.init()


class Screen:
    def __init__(self, size, background_color, title, space):
        self.background_color = background_color
        self.screen = pygame.display.set_mode(size)
        pygame.display.update()
        pygame.display.set_caption(title)

    def clear_screen(self):
        self.screen.fill(self.background_color)

    def update(self):
        pygame.display.flip()
