from pygame import time


class Timer:
    def __init__(self):
        self.started: bool = False
        self.target_time: int | float = 0
        self.starting_time: int | float = 0
        self.ending_time: int | float = 0
        self.timer_finished: bool = False
        self.seconds_restarted: int = 0
        self.function_target_time = 0

    def update_target_time(self, target_time, end_song_delay=0, ms=False) -> None:
        if ms:
            self.target_time += target_time - end_song_delay
        else:
            self.target_time += int(target_time) - end_song_delay

    def reset_time(self):
        self.starting_time = 0
        self.ending_time = 0

    def restart(self):
        self.seconds_restarted = self.ms_to_second(time.get_ticks())

    @staticmethod
    def ms_to_second(ms):
        return ms // 1000

    @property
    def current_time(self):
        return self.ms_to_second(time.get_ticks()) - self.seconds_restarted

    def compute_time(self):
        if self.current_time == self.target_time:
            self.timer_finished = True

    def start_time_ms(self):
        self.starting_time = time.get_ticks()
        self.started = True

    def end_time_ms(self):
        self.ending_time = time.get_ticks()

    @property
    def get_current_ms(self):
        return time.get_ticks()

    def get_time_spent(self) -> int | float:
        if not self.started:
            return 0
        return self.get_current_ms - self.starting_time

    def compute_ms_time(self):
        if self.get_current_ms >= self.target_time:
            self.timer_finished = True

    def init_delay_function(self, time_delay: int | float = 1000):
        self.function_target_time = time.get_ticks() + time_delay

    def activate_function(self, function):
        if time.get_ticks() >= self.function_target_time:
            function()

    @staticmethod
    def delay_func(function, time_delay: int | float = 1000):
        def exec_function():
            time.wait(time_delay)
            function()

        return exec_function


@Timer.delay_func
def print_hello():
    print("hello")


class MiniTimer:
    def __init__(self):
        self.last_time: int = time.get_ticks()


if __name__ == "__main__":
    print_hello()
    print("jasda")
