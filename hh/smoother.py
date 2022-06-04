import math

import cv2
import numpy as np


class SmootherKF:
    def __init__(self):
        self.filter = cv2.KalmanFilter(2, 1, 0)
        self.filter.transitionMatrix = np.array([[1, 1],
                                                 [0, 1]], dtype=np.float32)
        self.filter.measurementMatrix = np.array([[1, 1]], dtype=np.float32)
        self.filter.processNoiseCov = np.array([[1, 0],
                                                [0, 1]], dtype=np.float32) * 0.1
        self.filter.measurementNoiseCov = np.array([[1]], dtype=np.float32) * 0.1

        self.measurement = np.zeros((1, 1), dtype=np.float32)
        self.prediction = np.zeros((2, 1), dtype=np.float32)

        self.state = 0.0

    def update(self, measurement, dt):
        self.prediction = self.filter.predict()

        self.measurement = np.array([[np.float32(measurement)]])

        self.filter.correct(self.measurement)

        self.state = self.filter.statePost[0][0]


class SmootherDEMA:
    def __init__(self, a=0.06):
        self.a = a

        self.ema_ema = 0.0
        self.ema = 0.0

        self.state = 0.0

    def update(self, measurement, dt):
        self.ema = ema(self.a, measurement, self.ema)
        self.ema_ema = ema(self.a, self.ema, self.ema_ema)

        self.state = (2.0 * self.ema) - self.ema_ema


class SmootherTEMA:
    def __init__(self, a=0.06):
        self.a = a

        self.ema_ema_ema = 0.0
        self.ema_ema = 0.0
        self.ema = 0.0

        self.state = 0.0

    def update(self, measurement, dt):
        self.ema = ema(self.a, measurement, self.ema)
        self.ema_ema = ema(self.a, self.ema, self.ema_ema)
        self.ema_ema_ema = ema(self.a, self.ema_ema, self.ema_ema_ema)

        self.state = (3.0 * self.ema) - (3.0 * self.ema_ema) + self.ema_ema_ema


def ema(a, l, s):
    return (a * l) + ((1.0 - a) * s)


class SmootherOneEuro:
    def __init__(self, min_cutoff=1.0, beta=0.0, d_cutoff=1.0):
        self.min_cutoff = min_cutoff
        self.beta = beta
        self.d_cutoff = d_cutoff

        self.x_prev = 0.0
        self.dx_prev = 0.0

        self.state = 0.0

    def update(self, measurement, dt):
        a_d = smoothing_factor(dt, self.d_cutoff)
        dx = (measurement - self.x_prev) / dt
        dx_hat = exponential_smoothing(a_d, dx, self.dx_prev)

        cutoff = self.min_cutoff + self.beta * abs(dx_hat)
        a = smoothing_factor(dt, cutoff)
        x_hat = exponential_smoothing(a, measurement, self.x_prev)

        self.x_prev = x_hat
        self.dx_prev = dx_hat

        self.state = x_hat


def smoothing_factor(dt, cutoff):
    r = 2 * math.pi * cutoff * dt
    return r / (r + 1)


def exponential_smoothing(a, x, x_prev):
    return a * x + (1 - a) * x_prev

