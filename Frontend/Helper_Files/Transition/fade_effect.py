from pygame import Rect, draw
from Backend.timer import DelayTimer
from Frontend.settings import BLACK
from Frontend.Helper_Files.Transition.opacity import Opacity


class FadeEffect:
    __COLOR = BLACK
    __FADE_LEN_MS = 500
    __FADE_SPEED = 15

    def __init__(self, pos):
        self.__pos = pos
        self.__delay_timer = DelayTimer()
        self.__opacity = Opacity()
        self.__rect = Rect(0, 0, self.__pos.width, self.__pos.height)
        self.__finished_fade_in = False

    def show(self, screen, window):
        self.__update_rect()
        self.__draw_rect(screen=screen, window=window)
        self.__add_opacity()
        self.__check_if_finished_fade_in()
        self.__check_if_started_fading_out()

    def show_between_window(self, window):
        self.__update_rect()
        self.__draw_rect(window=window)
        self.__add_opacity()
        self.__check_if_finished_fade_in()
        self.__check_if_started_fading_out()

    def __update_rect(self):
        self.__rect = Rect(0, 0, self.__pos.width, self.__pos.height)

    def reset(self):
        self.__delay_timer.reset_timer()
        self.__opacity.reset_opacity()
        self.__finished_fade_in = False

    def __add_opacity(self):
        if self.finished_fade_in or self.start_fading_out:
            return
        self.__opacity.add_opacity(sum_num=self.__FADE_SPEED)

    def __draw_rect(self, window, screen=None):
        r, g, b = self.__COLOR
        if screen is None:
            draw.rect(window, (r, g, b, self.__opacity.opacity),
                      self.__rect)
        else:
            draw.rect(screen, (r, g, b, self.__opacity.opacity),
                      self.__rect)
            window.blit(screen, (0, 0))

    def __check_if_finished_fade_in(self):
        if self.finished_fade_in:
            self.__delay_timer.check_delay_ms(delay_ms=self.__FADE_LEN_MS)

    def __check_if_started_fading_out(self):
        if self.start_fading_out:
            self.__opacity.subtract_opacity(subtract_num=self.__FADE_SPEED)

    @property
    def finished_fade_in(self) -> bool:
        if self.__opacity.max_opacity:
            self.__finished_fade_in = True
        return self.__finished_fade_in

    @property
    def finished_fading_out(self) -> bool:
        return self.start_fading_out and self.__opacity.min_opacity

    @property
    def start_fading_out(self) -> bool:
        return self.__delay_timer.timer_finished

    @property
    def halfway_fade_out(self) -> bool:
        return self.__opacity.opacity <= 200 and self.start_fading_out
