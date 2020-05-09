import time
from simulation.environment import Environment
from simulation.agent import Agent
import pygame


class Simulation:
    def __init__(self, space, screen):
        self.screen = screen
        self.environment = Environment(space, screen)
        self.agents = []
        pass

    def iterate(self, t):
        self.environment.update()
        for a in self.agents:
            a.update(t)

    def display(self):
        self.screen.clear_screen()
        self.environment.display()
        [a.display() for a in self.agents]
        self.screen.update()

    def run(self, iterations, delay, iteration_time):
        """
        Run the simulation
        :param iterations:  number of iterations (-1 if infinite)
        :param delay: number of seconds of delay between each iteration
        :param iteration_time: amount of time passed every iteration (used to slow down movement speed)
        :return:
        """
        i = 0
        while i < iterations or iterations == -1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit
            start = time.time()
            self.iterate(iteration_time)
            self.display()
            time.sleep(max(0, delay - (time.time()-start))/1000)

    def create_random_agent(self, hidden_cells=10):
        creature = self.environment.new_creature()
        agent = Agent(creature, creature.get_input_count(), creature.get_output_count(), hidden_cells)
        self.agents.append(agent)
        return agent

    def create_agent_in_center(self, hidden_cells=1):
        creature = self.environment.new_creature_in_center()
        agent = Agent(creature, creature.get_input_count(), creature.get_output_count(), hidden_cells)
        self.agents.append(agent)
        return agent
