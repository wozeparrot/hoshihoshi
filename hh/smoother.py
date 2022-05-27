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

        self.state = 0.0
        self.measurement = np.zeros((1, 1), dtype=np.float32)
        self.prediction = np.zeros((2, 1), dtype=np.float32)

    def update(self, measurement):
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

    def update(self, measurement):
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

    def update(self, measurement):
        self.ema = ema(self.a, measurement, self.ema)
        self.ema_ema = ema(self.a, self.ema, self.ema_ema)
        self.ema_ema_ema = ema(self.a, self.ema_ema, self.ema_ema_ema)

        self.state = (3.0 * self.ema) - (3.0 * self.ema_ema) + self.ema_ema_ema


def ema(a, l, s):
    return (a * l) + ((1.0 - a) * s)
