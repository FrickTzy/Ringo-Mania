from pygame import Surface, SurfaceType, SRCALPHA, draw, mouse

from Backend import DelayTimer
from .left_side import LeftEndScreen
from .right_side import RightEndScreen
from .fade_effect import FadeEffect
from Frontend.settings import PURPLE, DARK_PURPLE


class EndScreen:
    def __init__(self, window_size: tuple[int, int], state, map_info):
        width, height = window_size
        self.pos = EndScreenPos(width=width, height=height)
        self.state = state
        self.__opacity = Opacity()
        self.__end_screen_surface = Surface((width, height), SRCALPHA)
        self.__fade_effect = FadeEffect(pos=self.pos, opacity=Opacity)
        self.__left_end_screen = LeftEndScreen(opacity=self.__opacity, end_screen=self.__end_screen_surface,
                                               pos=self.pos)
        self.__right_end_screen = RightEndScreen(end_screen=self.__end_screen_surface, pos=self.pos,
                                                 state=self.state, map_info=map_info)
        self.delay_timer = DelayTimer()
        self.__opacity.set_opacity(opacity=255)

    def show_end_screen(self, window: SurfaceType | Surface, size: tuple[int, int], stats: dict, date_time: dict,
                        grade):
        if self.__fade_effect.finished_fade_in:
            self.__end_screen_surface_setup(size=size)
            self.__add_bg_pause_surface()
            self.__draw_bottom_rect(color=DARK_PURPLE)
            self.__left_end_screen.show(end_screen=self.__end_screen_surface, stats=stats)
            self.__right_end_screen.show(end_screen=self.__end_screen_surface, date_time=date_time, grade=grade)
            window.blit(self.__end_screen_surface, (0, 0))
        self.__finished_delay_and_fade(window=window)

    def __finished_delay_and_fade(self, window):
        if self.__fade_effect.finished_fading_out:
            return
        self.delay_timer.check_delay_ms(delay_ms=1000)
        if self.delay_timer.timer_finished:
            self.__fade_effect.show(end_screen=self.__end_screen_surface, window=window)
            if self.__fade_effect.halfway_fade_out:
                mouse.set_visible(True)

    def restart(self):
        self.delay_timer.reset_timer()
        self.__fade_effect.reset()

    def __add_bg_pause_surface(self) -> None:
        r, g, b = PURPLE
        draw.rect(self.__end_screen_surface, (r, g, b, self.__opacity.opacity), (0, 0, self.pos.width, self.pos.height))

    def __end_screen_surface_setup(self, size: tuple[int, int]):
        width, height = size
        self.pos.update_window_size(width=width, height=height)
        self.__end_screen_surface = Surface((width, height), SRCALPHA)

    def __draw_bottom_rect(self, color):
        r, g, b = color
        draw.rect(self.__end_screen_surface, (r, g, b, self.__opacity.opacity),
                  (0, self.pos.bottom_rect_y, self.pos.width, self.pos.height))


class Opacity:
    __OPACITY_INTERVAL = 5

    def __init__(self):
        self.__opacity = 0

    @property
    def opacity(self) -> int:
        if self.__opacity > 255:
            self.__opacity = 255
        return self.__opacity

    @property
    def max_opacity(self) -> bool:
        return self.opacity == 255

    @property
    def min_opacity(self) -> bool:
        return self.__opacity <= 0

    def reset_opacity(self) -> None:
        self.__opacity = 0

    def set_opacity(self, opacity: int):
        self.__opacity = opacity

    def subtract_opacity(self, subtract_num: int = 5) -> None:
        if self.__opacity > 0:
            self.__opacity -= subtract_num

    def add_opacity(self, sum_num: int = 5) -> None:
        if self.__opacity < 255:
            self.__opacity += sum_num


class EndScreenPos:
    __BOTTOM_RECT_Y_RATIO = 1.23

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def update_window_size(self, width: int, height: int):
        self.width = width
        self.height = height

    @property
    def bottom_rect_y(self):
        return self.height // self.__BOTTOM_RECT_Y_RATIO
