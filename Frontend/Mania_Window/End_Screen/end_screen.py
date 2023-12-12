from pygame import Surface, SurfaceType, SRCALPHA, draw, mouse

from Backend import DelayTimer
from .left_side import LeftEndScreen
from Frontend.settings import PURPLE


class EndScreen:
    def __init__(self, window_size: tuple[int, int]):
        width, height = window_size
        self.pos = EndScreenPos(width=width, height=height)
        self.__opacity = Opacity()
        self.__end_screen_surface = Surface((width, height), SRCALPHA)
        self.__left_end_screen = LeftEndScreen(opacity=self.__opacity, end_screen=self.__end_screen_surface,
                                               pos=self.pos)
        self.delay_timer = DelayTimer()

    def show_end_screen(self, window: SurfaceType | Surface, size: tuple[int, int], stats: dict):
        self.delay_timer.check_delay_ms(delay_ms=800)
        if not self.delay_timer.timer_finished:
            return
        width, height = size
        self.__end_screen_surface_setup(width=width, height=height)
        self.__add_bg_pause_surface()
        self.__opacity.add_opacity()
        self.__left_end_screen.show(end_screen=self.__end_screen_surface, stats=stats["acc_dict"])
        window.blit(self.__end_screen_surface, (0, 0))
        if self.__opacity.opacity >= 50:
            mouse.set_visible(True)

    def restart(self):
        self.__opacity.reset_opacity()
        self.delay_timer.reset_timer()

    def __add_bg_pause_surface(self) -> None:
        r, g, b = PURPLE
        draw.rect(self.__end_screen_surface, (r, g, b, self.__opacity.opacity), (0, 0, self.pos.width, self.pos.height))

    def __end_screen_surface_setup(self, width: int, height: int):
        self.pos.update_window_size(width=width, height=height)
        self.__end_screen_surface = Surface((width, height), SRCALPHA)


class Opacity:
    __OPACITY_INTERVAL = 5

    def __init__(self):
        self.__opacity = 0

    @property
    def opacity(self):
        return self.__opacity

    def reset_opacity(self) -> None:
        self.__opacity = 0

    def add_opacity(self):
        if self.__opacity < 255:
            self.__opacity += 5


class EndScreenPos:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def update_window_size(self, width: int, height: int):
        self.width = width
        self.height = height
