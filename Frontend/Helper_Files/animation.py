from time import sleep


class Animation:
    __MAX_TIME: float = 1.01
    __current_seconds: float = 0
    __finished = False

    def __init__(self, ms_interval_per_iteration: float, timer):
        self.__ms_interval_per_iteration = ms_interval_per_iteration
        self.__timer = timer

    @staticmethod
    def smooth_in_animation(seconds_time: float):
        if seconds_time <= .5:
            return 2 * seconds_time * seconds_time
        seconds_time -= .5
        return 2 * seconds_time * (1 - seconds_time) + .5

    def run(self):
        self.__check_if_finished()
        if self.__finished:
            return
        self.smooth_in_animation(seconds_time=self.__current_seconds)
        self.__current_seconds += self.__ms_interval_per_iteration
        sleep(self.__ms_interval_per_iteration)

    def __check_if_finished(self):
        if self.__current_seconds > self.__MAX_TIME:
            self.__finished = True
