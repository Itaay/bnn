import numpy as np


def search_closest(a, l, n=1):
    result = sorted(l, key=lambda b: a.distance(b))
    if result[0] == a:
        result = result[1:]
    return result[:n]


def clip_color(c):
    return tuple(min(255, max(0, int(a))) for a in c)


def vector_size(a):
    return np.sqrt(np.sum(a**2))


def distance(a, b):
    return vector_size(b-a)
