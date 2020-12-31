from simulation.simulation import Simulation
from display.screen import Screen
from brain.space import Volume
import numpy as np


screen_size = np.array([600, 600])
BACKGROUND_COLOR = (154, 154, 158)
RECORD_SETTINGS = ("gallery/imgs", "gallery/videos", "result", 24)
space = Volume(shape='rect', location=np.array([0, 0, 0]), size=screen_size)
sim = Simulation(space, Screen(screen_size, BACKGROUND_COLOR, "GENERIC SIMULATION NAME", space, RECORD_SETTINGS))

for i in range(1):
    sim.create_random_agent(14)

for i in range(300):
    sim.environment.generate_new_food()

sim.run(-1, 1, 0.5)


