import numpy as np
import pygame
ID = 0
EPSIL = 0.00001
CHARGE_LIFE_TIME = 100


def get_id():
    global ID
    tmp = ID
    ID += 1
    return tmp


def number_of_charges():
    return ID


class Charge:
    def __init__(self, q, v, sender, receiver, bridge):
        self.ID = get_id()
        self.q = q
        self.v = v
        self.life_time = 0.0
        self.sender = sender
        self.receiver = receiver
        self.displacement = 0.0
        self.bridge = bridge

    def update(self, new_v=None):
        """
        Update the charge(simulation tick)
        :param new_v: Optional parameter, for if the speed of the charge has changed
        :return:
        """
        if new_v is not None:
            self.v = new_v
        self.life_time += 1
        self.displacement += self.v
        self.q = 0.99 * self.q
        self.v = self.bridge.get_speed(self.q)

    def reached(self, a):
        """
        whether the charge has reached the spot a
        :param a:
        :return:
        """
        return self.displacement >= a

    def doomed(self):
        return self.v <= EPSIL or self.life_time > CHARGE_LIFE_TIME

    def draw(self, screen):
        line_direction = self.receiver.location - self.sender.location  # get the difference between two endpoints
        if not np.all(line_direction == 0):
            line_direction = line_direction / np.sqrt(np.sum(line_direction**2))    # normalize
        point = self.sender.location + (line_direction*self.displacement)
        pygame.draw.circle(screen, np.maximum(np.minimum(np.array(np.array([2550, 2550, 2550])*self.q, dtype=int), 255), 0), np.array(point, dtype=int), 5)


