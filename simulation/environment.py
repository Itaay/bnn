from creature_simulation.creature import Creature
from .agent import Agent
from skeleton.node import Node
from creature_simulation.food import Food
import random


class Environment:
    def __init__(self, space, screen):
        self.space = space
        self.screen = screen
        self.food = []
        self.chance_to_generate_food = 0.2

    def update(self):
        chance = random.random()
        if chance <= self.chance_to_generate_food and len(self.food) < 1000:
            self.generate_new_food()
        for f in self.food:
            f.update()
            if f.age > f.max_age:
                self.food.remove(f)


    def display(self):
        for f in self.food:
            f.display()

    def new_creature(self):
        creature = Creature(self.space.random_loc(), self)
        return creature

    def new_creature_in_center(self):
        creature = Creature(self.space.center(), self)
        return creature

    def generate_new_food(self):
        new_food = Food(self, Node(self.space.random_loc(), self.space, None))
        self.food.append(new_food)

