import numpy as np
from skeleton.node import Node
DEG2RAD = np.pi / 180.0


class Volume:
    def __init__(self, shape, location, size, in_degrees=True):
        self.location = location
        self.size = np.array(size)
        self.kind = shape
        self.in_degrees = in_degrees

    def random_loc(self):
        if self.kind == 'rect':
            # the location is [x,y,rotation] of top left corner
            place = np.zeros(3) # in case rotation not given, pad
            place[:self.location.shape[0]] = self.location
            spot = np.random.random(2)*self.size    # get a random location on the rect's area
            spot = rotate(spot, place[2], self.in_degrees)  # rotate based on rect rotation
            return place[:2]+spot   # translate spot on rect relative to top left position

    def is_in(self, p):
        if self.kind == 'rect':
            angle = 0.0
            if self.location.shape[0] == 3:
                angle = self.location[2]
            p = p-self.location[:2]
            p = rotate(p, -angle, self.in_degrees)
            return np.all(0 <= p <= self.location[:2])

    def origin(self):
        if self.kind == 'rect':
            return None
            return Node(np.zeros(2), self, None)

    def start_direction(self):
        if self.kind == 'rect':
            return np.array([1,0])

    def default_direction(self):
        if self.kind == 'rect':
            return 0

    def rotate(self, a, b):
        """
        Rotate the vector b based on the parent a
        :param a: parent vector
        :param b: child vector
        :return: result
        """
        if self.kind =='rect':
            a_loc = a
            alpha = np.arctan2(-a_loc[0], a_loc[1])
            return rotate(b, alpha, False)

    def center(self):
        if self.kind == 'rect':
            # not updated if rotated
            return self.location[:2] + (self.size/2)

    def out_of_bounds(self, a):
        if self.kind == 'rect':
            if np.any(a < 0) or np.any(a-self.size > 0):
                return True


def rotate(vec, alpha, in_degrees=True):
    """
    Rotate a given vector based on an angle.
    Uses matrix multiplication for calculation
    :param vec:         Vector to rotate
    :param alpha:       Angle to rotate
    :param in_degrees:  Angle format(boolean: If true, then degrees. If False, then radians)
    :return:            Rotated vector
    """
    if in_degrees:
        alpha = alpha*DEG2RAD
    sinus = np.sin(alpha)
    cosinus = np.cos(alpha)
    rotation_matrix = np.array([[cosinus,-sinus],[sinus, cosinus]])
    result = np.dot(rotation_matrix, np.expand_dims(vec,axis=-1)).flatten()
    #   print("rot(" + str(vec) + ", " + str(alpha) + "): " + str(result))
    return result
