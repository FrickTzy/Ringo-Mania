from pygame import K_ESCAPE, time
from Stuff.Ringo_Mania.Frontend.falling_circles import FallingCircle
from Stuff.Ringo_Mania.Backend.music import Music
from Stuff.Ringo_Mania.Backend.timer import Timer


class Pause:
    __PAUSE_INTERVAL = 300

    def __init__(self, circles: list[FallingCircle], music: Music, mini_timer):
        self.__starting_time: int = 0
        self.__paused = False
        self.__circles = circles
        self.__music = music
        self.mini_timer = mini_timer
        self.timer = Timer()

    def check_pause(self, key_pressed) -> bool:
        current_time = time.get_ticks()
        if key_pressed[K_ESCAPE]:
            if current_time - self.__starting_time >= self.__PAUSE_INTERVAL:
                # print("escaped")
                self.__starting_time = current_time
                if self.__paused:
                    self.unpause()
                    self.timer.end_time_ms()
                    self.__paused = False
                    return False
                else:
                    self.timer.reset_time()
                    self.timer.start_time_ms()
                    self.__paused = True
                    return True

    @property
    def is_paused(self) -> bool:
        return self.__paused

    def show_pause(self) -> None:
        for circles in self.__circles:
            circles.draw_circle(pause=True)
            self.__music.pause_music()

    def unpause(self):
        self.__music.unpause_music()
        self.mini_timer.last_time += self.timer.get_time_spent()

    @property
    def time_spent_paused(self) -> int | float:
        return self.timer.get_time_spent()
