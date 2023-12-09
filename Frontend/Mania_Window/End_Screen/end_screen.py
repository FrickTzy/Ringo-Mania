from pygame import Surface, SurfaceType, SRCALPHA, draw, mouse
from Stuff.Ringo_Mania.Frontend.Mania_Window.settings import PURPLE


class EndScreen:
    __opacity = 0

    def __init__(self, window_size: tuple[int, int], window: Surface):
        width, height = window_size
        self.pos = EndScreenPos(width=width, height=height)
        self.__end_screen_surface = Surface((width, height), SRCALPHA)

    def show_end_screen(self, window: SurfaceType | Surface, stats: dict):
        self.__end_screen_surface_setup(width=self.pos.width, height=self.pos.height)
        self.__add_bg_pause_surface()
        window.blit(self.__end_screen_surface, (0, 0))
        mouse.set_visible(True)

    def __add_bg_pause_surface(self) -> None:
        r, g, b = PURPLE
        draw.rect(self.__end_screen_surface, (r, g, b, self.__opacity), (0, 0, self.pos.width, self.pos.height))
        if self.__opacity < 255:
            self.__opacity += 5

    def __end_screen_surface_setup(self, width: int, height: int):
        self.pos.update_window_size(width=width, height=height)
        self.__end_screen_surface = Surface((width, height), SRCALPHA)


class EndScreenPos:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def update_window_size(self, width: int, height: int):
        self.width = width
        self.height = height
