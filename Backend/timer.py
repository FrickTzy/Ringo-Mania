from pygame import time


class Timer:
    def __init__(self):
        self.started: bool = False
        self.target_time: int | float = 0
        self.current_time: int | float = 0
        self.starting_time: int | float = 0
        self.ending_time: int | float = 0
        self.timer_finished: bool = False
        self.function_target_time = 0

    def update_target_time(self, target_time, end_song_delay=0, ms=False) -> None:
        if ms:
            self.target_time += target_time - end_song_delay
        else:
            self.target_time += int(target_time) - end_song_delay

    def reset_time(self):
        self.starting_time = 0
        self.ending_time = 0

    @staticmethod
    def ms_to_second(ms):
        return ms / 1000

    def compute_time(self):
        self.current_time = int((self.ms_to_second(time.get_ticks())))
        if self.current_time == self.target_time:
            self.timer_finished = True

    def start_time_ms(self):
        self.starting_time = time.get_ticks()
        self.started = True

    def end_time_ms(self):
        self.ending_time = time.get_ticks()

    @staticmethod
    def get_current_ms():
        return time.get_ticks()

    def get_time_spent(self) -> int | float:
        if not self.started:
            return 0
        return self.get_current_ms() - self.starting_time

    def compute_ms_time(self):
        self.current_time = time.get_ticks()
        if self.current_time >= self.target_time:
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
