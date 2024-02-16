from .smoothing_methods import SmoothingInterface


class Animation:
    __MAX_TIME: float = 1.01
    __current_seconds: float = 0

    def __init__(self, ms_interval_per_iteration: float, smoothing_method: SmoothingInterface):
        self.__ms_interval_per_iteration = ms_interval_per_iteration
        self.__smoothing_method = smoothing_method

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
