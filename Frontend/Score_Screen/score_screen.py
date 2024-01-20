from pygame import Surface, SurfaceType, SRCALPHA, draw, mouse

from Backend import DelayTimer
from .left_side import LeftScoreScreen
from .right_side import RightScoreScreen
from Frontend.Helper_Files import FadeEffect, Opacity, State
from .background import Background
from Frontend.Settings import Color


class ScoreScreen:
    __SHOW_BACKGROUND = True
    __BACKGROUND_COLOR = Color.PURPLE
    __BOTTOM_RECT_COLOR = Color.DARK_PURPLE
    __fade_out = True

    def __init__(self, window_size: tuple[int, int], state: State, map_info):
        width, height = window_size
        self.pos = EndScreenPos(width=width, height=height)
        self.state: State = state
        self.score_screen = Surface((width, height), SRCALPHA)
        self.fade_effect = FadeEffect(pos=self.pos)
        self.__opacity = Opacity(opacity=255)
        self.__left_screen = LeftScoreScreen(opacity=self.__opacity, screen=self.score_screen,
                                             pos=self.pos)
        self.__map_info = map_info
        self.__right_screen = RightScoreScreen(screen=self.score_screen, pos=self.pos,
                                               state=self.state, map_info=self.__map_info)
        self.__background = Background()
        self.delay_timer = DelayTimer()

    def show_score_screen(self, window: SurfaceType | Surface, size: tuple[int, int], stats: dict, date_time: dict,
                          grade, has_delay=True):
        if self.fade_effect.finished_fade_in:
            self.show_screen(size=size, stats=stats, date_time=date_time, grade=grade)
            window.blit(self.score_screen, (0, 0))
        self.finished_delay_and_fade(window=window, has_delay=has_delay)

    def hide_score_screen(self, window: SurfaceType | Surface, size: tuple[int, int], stats: dict, date_time: dict,
                          grade, has_delay=True):
        if self.__fade_out:
            self.__reset_fade()
            self.__fade_out = False
        if not self.fade_effect.finished_fade_in:
            self.show_screen(size=size, stats=stats, date_time=date_time, grade=grade)
            window.blit(self.score_screen, (0, 0))
        if self.finished_delay_and_fade(window=window, has_delay=has_delay):
            self.state.finished_fade_out = True

    def show_screen(self, size: tuple[int, int], stats: dict, date_time: dict,
                    grade):
        self.__score_screen_setup(size=size)
        self.__add_bg_score_surface()
        self.__draw_bottom_rect(color=self.__BOTTOM_RECT_COLOR)
        self.__left_screen.show(screen=self.score_screen, stats=stats)
        self.__right_screen.show(screen=self.score_screen, date_time=date_time, grade=grade)

    def finished_delay_and_fade(self, window, has_delay: bool):
        if self.fade_effect.finished_fading_out:
            return True
        if has_delay:
            self.delay_timer.check_delay_ms(delay_ms=1000)
            if not self.delay_timer.timer_finished:
                return
        self.fade_effect.show(screen=self.score_screen, window=window)
        if self.fade_effect.halfway_fade_out:
            mouse.set_visible(True)

    def __reset_fade(self):
        self.delay_timer.reset_timer()
        self.fade_effect.reset()

    def restart(self):
        self.delay_timer.reset_timer()
        self.fade_effect.reset()
        self.__fade_out = True
        self.state.finished_fade_out = False

    def __add_bg_score_surface(self) -> None:
        r, g, b = self.__BACKGROUND_COLOR
        draw.rect(self.score_screen, (r, g, b, self.__opacity.opacity), (0, 0, self.pos.width, self.pos.height))
        if self.__SHOW_BACKGROUND:
            self.__background.show_background(screen=self.score_screen, window_size=self.pos.window_size,
                                              background_image=self.__map_info.current_background_image)

    def __score_screen_setup(self, size: tuple[int, int]):
        width, height = size
        self.pos.update_window_size(width=width, height=height)
        self.score_screen = Surface((width, height), SRCALPHA)

    def __draw_bottom_rect(self, color):
        r, g, b = color
        draw.rect(self.score_screen, (r, g, b, self.__opacity.opacity),
                  (0, self.pos.bottom_rect_y, self.pos.width, self.pos.height))


class EndScreenPos:
    __BOTTOM_RECT_Y_RATIO = 1.23

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def update_window_size(self, width: int, height: int):
        self.width = width
        self.height = height

    @property
    def window_size(self):
        return self.width, self.height

    @property
    def bottom_rect_y(self):
        return self.height // self.__BOTTOM_RECT_Y_RATIO
