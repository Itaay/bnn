from brain.charge import Charge
import pygame
import numpy as np
from utils import *
ID = 0


def get_id():
    global ID
    tmp = ID
    ID += 1
    return tmp


class Synapse:
    def __init__(self, start, end, strength=0.0):
        self.id = get_id()                          #   Id of synapse object
        self.start_point = start                    #   The instance of the outputting neuron(that transmits the signal)
        self.end_point = end                        #   The instance of the receiving neuron
        self.strength = strength                    #   The strength of the connection
        self.starting_strength = strength           #   The initial strength of the connection
        self.signals = []                           #   List of current signals in the Synapse
        self.activity = 0.0                         #   Activity score of synapse(How much charge in average is in the bridge)
        self.strain = 0.0
        self.activity_decay = 0.01                   #   Activity decay rate: How quickly the moving average decays
        self.strength_grow_rate = 0.01               #   How quickly the strength of the synapse grows
        self.strength_decay_rate = 0.0001        #   How quickly the strength of the synapse degrades
        self.activity_bottleneck_threshold = 0.25    #   activity/strength ratio threshold after which needs to strengthen
        self.redundancy_threshold = 0.01           #   activity/strength lower boundary: if below, reduce strength
        self.max_strength = 0.5
        self.can_learn = True

        self.tension = 0.0

    def set_learning_state(self, state):
        self.can_learn = state

    def max_charge(self):
        """
        Get the maximum charge that can go through this bridge.
        For now, it's determined only by current strength of the bridge, so let's say it equals to it.
        Might change in the future if needed to
        :return:
        """
        return self.strength

    def get_speed(self, c):
        """
        Get the speed a charge will move at.
        v = strength/c
        That way, the bigger the charge is, the slower it will take to travel,
        but the stronger the connection is, the faster it will be.
        :param c: The charge size
        :return:
        """
        return self.strength / (abs(c)+0.000001)

    def set_strength(self, new_strength):
        self.strength = new_strength
        self.cap_strength()
        for s in self.signals:
            s.v = self.get_speed(s.q)

    def fire(self, c):
        """
        fire a signal through the synapse
        :param c: the charge of the wanted signal
        :return:
        """
        if c == 0:
            return 0.0
        sign = c / abs(c)
        charge_size = min(abs(c), max(0, self.max_charge()*0.5 - self.current_activity()))
        if charge_size > 0.01:
            signal = Charge(sign * charge_size, self.get_speed(charge_size), self.start_point, self.end_point, self)
            self.signals.append(signal)
        else:
            charge_size = 0.0
        return charge_size

    def update_strength(self):
        usefulness_ratio = self.activity / self.strength
        if usefulness_ratio > self.activity_bottleneck_threshold:
            wanted_strength = self.activity / self.activity_bottleneck_threshold
            self.set_strength(self.strength_grow_rate*wanted_strength + (1-self.strength_grow_rate)*self.strength)
        if usefulness_ratio < self.redundancy_threshold:
            wanted_strength = max(self.starting_strength, self.activity / self.redundancy_threshold)
            self.set_strength(self.strength_decay_rate*wanted_strength + (1-self.strength_decay_rate)*self.strength)

    def cap_strength(self):
        self.strength = max(self.starting_strength, min(self.max_strength, self.strength))

    def current_activity(self):
        """
        How much charge is currently transported through the bridge
        """
        return sum([abs(s.q) for s in self.signals])

    def update_activity(self, decay=None):
        noise_level = 0.0
        if decay is None:
            decay = self.activity_decay
        current_activity = self.current_activity()
        self.activity = (1-decay)*self.activity + decay*current_activity
        self.activity += (np.random.random()*(2*noise_level*self.activity)) - noise_level*self.activity
        self.strain = self.current_activity() / self.strength #     / self.max_charge()
        return self.activity

    def update(self):
        i = 0
        while i < len(self.signals):
            signal = self.signals[i]
            signal.update()
            if signal.reached(self.distance()):
                self.end_point.absorb(signal)
                self.signals.remove(signal)
            elif signal.doomed():
                self.signals.remove(signal)
            else:
                i += 1
        self.update_activity()
        self.pull_end_points()
        if self.can_learn:
            self.update_strength()
        self.cap_strength()

    def reinforce(self, reward, depth=0):
        self.start_point.reward(reward, depth)  # reward the starting end of the dendrite
        if self.can_learn:
            self.tension += reward
            self.set_strength(self.strength + reward)
        self.cap_strength()

    def draw(self, screen):
        self.draw2d(screen)

    def draw2d(self, screen):
        for s in self.signals:
            s.draw(screen)
        pygame.draw.line(screen, clip_color((0, 255*self.strength, 255*self.strength)), np.array(self.start_point.location, dtype=int), np.array(self.end_point.location, dtype=int), 4)

    def distance(self):
        return self.start_point.distance(self.end_point)  # The distance between the two endpoints

    def pull_end_points(self):
        delta = self.end_point.location - self.start_point.location
        direction = delta / self.distance()
        force = self.pull_activation(self.tension / 2) * direction
        self.start_point.location += force
        self.end_point.location -= force
        self.tension = 0

    def pull_activation(self, a):
        return min(a*np.exp(min(10, 0.05*a*self.distance())), 50)





