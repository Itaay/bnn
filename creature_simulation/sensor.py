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
        boost = 1
        foods = self.environment.food
        self.value = 0.0
        distances = sorted([distance(self.location_node.location(), food.position.location()) for food in foods])

        for d in distances[:1]:
            self.value += boost / (d+0.0001)
        """for food in foods:
            distance_to_food = distance(self.location_node.location(), food.position.location())
            if distance_to_food < 50:
                self.value += boost / distance_to_food
                """
        return self.value

    def display(self):
        # draw a line to the parent origin
        pygame.draw.line(self.environment.screen.screen, (0,0,0), self.location_node.parent.location(), self.location_node.location(), 3)
        # draw a circle in the location
        pygame.draw.circle(self.environment.screen.screen, self.color, np.array(self.location_node.location(), dtype=int), 5)
        pass
