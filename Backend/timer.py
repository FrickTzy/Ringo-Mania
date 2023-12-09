from pygame import time


class Timer:
    def __init__(self):
        self.started: bool = False
        self.target_time: int | float = 0
        self.starting_time: int | float = 0
        self.ending_time: int | float = 0
        self.timer_finished: bool = False
        self.seconds_restarted: int = 0

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


class DelayTimer:
    def __init__(self):
        self.__start_time: int | float = 0
        self.__started_timer = False
        self.__timer_finished: bool = False

    def check_delay(self, delay_seconds):
        if not self.__started_timer:
            self.__start_time = self.current_seconds
            self.__started_timer = True
        if self.__start_time + delay_seconds <= self.current_seconds:
            self.__timer_finished = True

    @property
    def timer_finished(self):
        return self.__timer_finished

    @property
    def current_seconds(self):
        return self.ms_to_second(time.get_ticks())

    @staticmethod
    def ms_to_second(ms):
        return ms // 1000


class IntervalTimer:
    def __init__(self, interval: int = 100):
        self.last_time: int = time.get_ticks()
        self.interval = interval

    def time_interval_finished(self) -> bool:
        current_time = time.get_ticks()
        if current_time - self.last_time >= self.interval:
            self.last_time = current_time
            return True

    def change_interval(self, interval):
        self.interval = interval
