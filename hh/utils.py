import sys

import numpy as np


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def lerp(c, a, b):
    return ((1 - c) * a) + (c * b)


def remap(x, m, M):
    return (max(m, min(x, M)) - m) / (M - m)


def norm_angle(x):
    a = x % (2 * np.pi)
    if a > np.pi:
        a -= 2 * np.pi
    elif a < -np.pi:
        a += 2 * np.pi
    return a / np.pi
