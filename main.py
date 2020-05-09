from simulation.simulation import Simulation
from display.screen import Screen
from brain.space import Volume
import numpy as np


screen_size = np.array([1800, 1000])
BACKGROUND_COLOR = (154, 154, 158)
space = Volume(shape='rect', location=np.array([0, 0, 0]), size=screen_size)
sim = Simulation(space, Screen(screen_size, BACKGROUND_COLOR, "GENERIC SIMULATION NAME", space))

for i in range(1):
    sim.create_random_agent(2)

for i in range(500):
    sim.environment.generate_new_food()

sim.run(-1, 1, 0.5)


