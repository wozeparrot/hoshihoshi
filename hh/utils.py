import sys


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def lerp(c, a, b):
    return ((1 - c) * a) + (c * b)


def remap(x, m, M):
    return (max(m, min(x, M)) - m) / (M - m)
