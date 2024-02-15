from abc import ABC, abstractmethod
from math import pow


class Animation:
    __MAX_TIME: float = 1.01
    __current_seconds: float = 0

    def __init__(self, ms_interval_per_iteration: float):
        self.__ms_interval_per_iteration = ms_interval_per_iteration
        self.__smoothing_method: SmoothingInterface = EaseOutCubicSmoothing()

    def run(self):
        if self.__finished():
            return
        self.__smoothing_method.smooth_in_animation(seconds_time=self.__current_seconds)
        self.__current_seconds += self.__ms_interval_per_iteration

    def get_current_percentage(self):
        if self.__finished():
            return 1
        percentage = self.__smoothing_method.smooth_in_animation(seconds_time=self.__current_seconds)
        self.__current_seconds += self.__ms_interval_per_iteration
        return percentage

    def __finished(self):
        if self.__current_seconds > self.__MAX_TIME:
            return True
        return False

    def reset(self):
        self.__current_seconds = 0

    def change_interval(self, ms_interval: float):
        self.__ms_interval_per_iteration = ms_interval


class SmoothingInterface(ABC):
    @staticmethod
    @abstractmethod
    def smooth_in_animation(seconds_time: float):
        pass


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
