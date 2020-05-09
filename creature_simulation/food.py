import pygame
import numpy as np


class Food:
    def __init__(self, environment, pos):
        self.position = pos
        self.environment = environment
        self.color = (110, 64, 12)
        self.age = 0
        self.max_age = 1000000

    def display(self):
        pygame.draw.circle(self.environment.screen.screen, self.color, np.array(self.position.location(), dtype=int), 6)

    def update(self):
        self.age += 1
