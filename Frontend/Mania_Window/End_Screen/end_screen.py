from pygame import Surface, SurfaceType, SRCALPHA, draw, mouse

from Backend import DelayTimer
from Frontend.Mania_Window.End_Screen.left_side import StatsText
from Frontend.settings import PURPLE


class EndScreen:
    def __init__(self, window_size: tuple[int, int], font):
        width, height = window_size
        self.pos = EndScreenPos(width=width, height=height)
        self.__opacity = Opacity()
        self.__end_screen_surface = Surface((width, height), SRCALPHA)
        self.__stats_text = StatsText(end_screen_surface=self.__end_screen_surface, font=font, screen_pos=self.pos,
                                      opacity=self.__opacity)
        self.delay_timer = DelayTimer()

    def show_end_screen(self, window: SurfaceType | Surface, stats: dict):
        self.delay_timer.check_delay(delay_seconds=2)
        if not self.delay_timer.timer_finished:
            return
        self.__end_screen_surface_setup(width=self.pos.width, height=self.pos.height)
        self.__add_bg_pause_surface()
        self.__stats_text.show_text(end_screen_surface=self.__end_screen_surface)
        self.__opacity.add_opacity()
        window.blit(self.__end_screen_surface, (0, 0))
        mouse.set_visible(True)

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
