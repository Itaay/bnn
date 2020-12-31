from brain import colony

import random


class Agent:
    def __init__(self, creature, wanted_input_cells, wanted_output_cells, hidden_neurons):
        self.brain = colony.default_generate(wanted_input_cells + wanted_output_cells + hidden_neurons)
        self.input_cells = []
        self.output_cells = []
        self.creature = creature
        self.allocate_io_cells(wanted_input_cells, wanted_output_cells)

    def allocate_io_cells(self, wanted_input_cells, wanted_output_cells):
        assert wanted_input_cells + wanted_output_cells <= len(self.brain.cells)
        # get [wanted_input_cells + wanted_output_cells] random numbers in the range and allocate them accordingally
        io_cells = random.sample(range(len(self.brain.cells)), wanted_input_cells + wanted_output_cells)
        self.input_cells = [self.brain.cells[i] for i in io_cells[:wanted_input_cells]]
        self.output_cells = [self.brain.cells[i] for i in io_cells[wanted_input_cells:]]
        for i in self.input_cells:
            i.color = (0, 0, 255)

        output_callbacks = self.creature.get_output_actions()
        for i in range(len(self.output_cells)):
            self.output_cells[i].color = (0, 255, 0)
            self.output_cells[i].fire_callback = output_callbacks[i]

    def feed_inputs(self, inputs):
        for i in range(len(self.input_cells)):
            self.input_cells[i].feed_charge(inputs[i])

    def get_output(self):
        return [c.state for c in self.output_cells]

    def update(self, t):
        inputs = self.creature.get_inputs()
        self.brain.update(15)
        self.feed_inputs(inputs)
        outputs = self.get_output()
        self.creature.use_outputs(outputs)
        self.creature.update(t)

        activity_sum = sum([c.average_charge for c in self.output_cells])
        for c in self.output_cells:
            c.reward(self.creature.happiness * c.average_charge )#   / (activity_sum+0.001))

    def display(self):
        self.brain.draw(self.creature.environment.screen.screen)
        self.creature.display()
