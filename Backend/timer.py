from pygame import time


class Timer:
    def __init__(self):
        self.target_time = 0
        self.current_time = 0
        self.timer_finished = False

    def update_target_time(self, target_time, end_song_delay=0):
        self.target_time += int(target_time) - end_song_delay

    @staticmethod
    def ms_to_second(ms):
        return ms / 1000

    def compute_time(self):
        self.current_time = int((self.ms_to_second(time.get_ticks())))
        if self.current_time == self.target_time:
            self.timer_finished = True
