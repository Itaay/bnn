from skeleton.node import Node
from .sensor import Sensor
import numpy as np
from brain.space import rotate
import pygame
from utils import vector_size, distance


class Creature:
    def __init__(self, location, environment):
        self.environment = environment
        self.position = Node(location, environment.space, environment.space.origin())
        self.sensors = []

        # add sensors to the creatures
        self.sensors.append(Sensor(environment, Node(np.array([10, 10]), environment.space, self.position)))
        self.sensors.append(Sensor(environment, Node(np.array([-10, 10]), environment.space, self.position)))
        self.sensors.append(Sensor(environment, Node(np.array([0, 14.142]), environment.space, self.position)))

        #   self.v = np.zeros(2)
        self.v = np.array([0, 5])
        self.max_speed = 2

        self.color = (35, 140, 20)

        self.happiness = 0
        self.radius = 10
        self.stuff_eaten = 0
        self.food_happiness = 1.5

    def get_input_count(self):
        return len(self.sensors)

    def get_output_count(self):
        return 2

    def get_inputs(self):
        return [s.sense() for s in self.sensors]

    def use_outputs(self, outputs):
        """left = outputs[0]
        right = outputs[1]

        rotation = (right - left) / 1.5
        #   self.v = self.position.direction * max(0.001, accelerate) * 10
        #   print(self.v)
        self.v = rotate(self.v, rotation, False)"""
        self.position.direction = self.v / vector_size(self.v)

    def get_output_actions(self):
        boost = 1.0

        def rotate_right(power):
            self.rotate(boost*power)

        def rotate_left(power):
            self.rotate(-boost*power)

        return [rotate_left, rotate_right]

    def rotate(self, rotation):
        self.v = rotate(self.v, rotation, False)

    def display(self):
        # display the creature
        pygame.draw.circle(self.environment.screen.screen, self.color, np.array(self.position.location(), dtype=int), self.radius)
        # display the creature's sensors
        for s in self.sensors:
            s.display()
        pass

    def update(self, t):
        self.position.move(self.v * t)
        #   self.happiness /= 3
        self.happiness = 0.0
        self.try_eat_food()
        if self.environment.space.out_of_bounds(self.position.location()):
            self.position.offset = self.environment.space.center()

    def try_eat_food(self):
        for f in self.environment.food:
            if distance(self.position.location(), f.position.location()) < self.radius * 2:
                self.stuff_eaten += 1
                self.happiness += self.food_happiness
                #   self.food_happiness *= 0.95

                self.environment.food.remove(f)


