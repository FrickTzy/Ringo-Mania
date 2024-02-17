from .smoothing_interface import SmoothingInterface
from math import pow


class QuadraticSmoothing(SmoothingInterface):
    @staticmethod
    def smooth_in_animation(seconds_time: float):
        if seconds_time <= .5:
            return 2 * seconds_time * seconds_time
        seconds_time -= .5
        return 2 * seconds_time * (1 - seconds_time) + .5


class ParametricSmoothing(SmoothingInterface):
    @staticmethod
    def smooth_in_animation(seconds_time: float):
        square = seconds_time * seconds_time
        return square / (2.0 * (square - seconds_time) + 1.0)


class EaseOutQuintSmoothing(SmoothingInterface):
    @staticmethod
    def smooth_in_animation(seconds_time: float):
        return 1 - pow(1 - seconds_time, 5)


class EaseOutCubicSmoothing(SmoothingInterface):
    @staticmethod
    def smooth_in_animation(seconds_time: float):
        return 1 - pow(1 - seconds_time, 3)


class EaseOutBackSmoothing(SmoothingInterface):
    @staticmethod
    def smooth_in_animation(seconds_time: float):
        c1 = 1.70158
        c3 = c1 + 1
        return 1 + c3 * pow(seconds_time - 1, 3) + c1 * pow(seconds_time - 1, 2)
