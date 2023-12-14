from pygame import draw
from .acc_text import AccText
from .acc_logo import AccLogo
from Frontend.settings import DARK_PURPLE


class LeftEndScreen:
    def __init__(self, *, opacity, end_screen, pos):
        self.__acc_text = AccText(end_screen_surface=end_screen, screen_pos=pos,
                                  opacity=opacity)
        self.__acc_logo = AccLogo(screen_pos=pos, opacity=opacity)
        self.__background = EndScreenBackground(pos=pos, opacity=opacity)

    def show(self, end_screen, stats):
        self.__background.draw_to_pause_surface(end_screen=end_screen)
        self.__acc_text.show_text(end_screen_surface=end_screen, stats=stats)
        self.__acc_logo.show_logo(end_screen_surface=end_screen)


class EndScreenBackground:
    __COLOR = DARK_PURPLE

    def __init__(self, pos, opacity):
        self.__pos = BackgroundRectanglePos(pos=pos)
        self.__opacity = opacity

    def draw_to_pause_surface(self, end_screen) -> None:
        self.__draw_background_rect(end_screen=end_screen, y=self.__pos.get_rect_y(sequence_num=1), color=self.__COLOR)
        self.__draw_background_rect(end_screen=end_screen, y=self.__pos.get_rect_y(sequence_num=2), color=self.__COLOR)
        self.__draw_background_rect(end_screen=end_screen, y=self.__pos.get_rect_y(sequence_num=3), color=self.__COLOR)

    def __draw_background_rect(self, end_screen, y, color):
        r, g, b = color
        draw.rect(end_screen, (r, g, b, self.__opacity.opacity),
                  (self.__pos.padding, y, self.__pos.width, self.__pos.height))


class BackgroundRectanglePos:
    __HEIGHT_RATIO = 7.5
    __PADDING_RATIO = 53.33
    __RECT_INTERVAL_RATIO = 5.5
    __STARTING_Y_RATIO = 4.74

    def __init__(self, pos):
        self.__pos = pos

    @property
    def width(self):
        return (self.__pos.width // 2) - (self.padding * 2)

    @property
    def height(self):
        return self.__pos.height // self.__HEIGHT_RATIO

    @property
    def padding(self):
        return self.__pos.width // self.__PADDING_RATIO

    @property
    def __rect_interval(self):
        return self.__pos.height // self.__RECT_INTERVAL_RATIO

    @property
    def __starting_y(self):
        return self.__pos.height // self.__STARTING_Y_RATIO

    def get_rect_y(self, sequence_num: int):
        return self.__starting_y + (self.__rect_interval * (sequence_num - 1))
