import pygame
import numpy as np
from utils import distance


class Sensor:
    def __init__(self, environment, location):
        self.environment = environment
        self.value = 0.0
        self.location_node = location

        self.color = (50, 30, 140)

    def sense(self):
        boost = 100
        foods = self.environment.food
        self.value = sum([boost / (distance(self.location_node.location(), food.position.location())**2) for food in foods])
        return self.value

    def display(self):
        # draw a line to the parent origin
        pygame.draw.line(self.environment.screen.screen, (0,0,0), self.location_node.parent.location(), self.location_node.location(), 3)
        # draw a circle in the location
        pygame.draw.circle(self.environment.screen.screen, self.color, np.array(self.location_node.location(), dtype=int), 5)
        pass
