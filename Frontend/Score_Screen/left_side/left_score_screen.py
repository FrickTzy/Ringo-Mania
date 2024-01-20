from pygame import draw
from .acc_text import AccText
from .acc_logo import AccLogo
from Frontend.Settings import Color


class LeftScoreScreen:
    def __init__(self, *, opacity, screen, pos):
        self.__acc_text = AccText(screen_surface=screen, screen_pos=pos,
                                  opacity=opacity)
        self.__acc_logo = AccLogo(screen_pos=pos, opacity=opacity)
        self.__background = ScoreScreenBackground(pos=pos, opacity=opacity)

    def show(self, screen, stats):
        self.__background.draw_to_pause_surface(screen=screen)
        self.__acc_text.show_text(screen_surface=screen, stats=stats)
        self.__acc_logo.show_logo(screen_surface=screen)


class ScoreScreenBackground:
    __COLOR = Color.DARK_PURPLE

    def __init__(self, pos, opacity):
        self.__pos = BackgroundRectanglePos(pos=pos)
        self.__opacity = opacity

    def draw_to_pause_surface(self, screen) -> None:
        self.__draw_top_rect(screen=screen, color=self.__COLOR)
        self.__draw_background_rect(screen=screen, y=self.__pos.get_rect_y(sequence_num=1), color=self.__COLOR)
        self.__draw_background_rect(screen=screen, y=self.__pos.get_rect_y(sequence_num=2), color=self.__COLOR)
        self.__draw_background_rect(screen=screen, y=self.__pos.get_rect_y(sequence_num=3), color=self.__COLOR)
        # self.__draw_background_rect(screen=screen, y=self.__pos.get_rect_y(sequence_num=4),
        # color=self.__COLOR)

    def __draw_background_rect(self, screen, y, color):
        r, g, b = color
        draw.rect(screen, (r, g, b, self.__opacity.opacity),
                  (self.__pos.padding, y, self.__pos.width, self.__pos.height))

    def __draw_top_rect(self, screen, color):
        r, g, b = color
        draw.rect(screen, (r, g, b, self.__opacity.opacity),
                  (0, 0, self.__pos.top_rect_width, self.__pos.top_rect_height))


class BackgroundRectanglePos:
    __HEIGHT_RATIO = 7.5
    __PADDING_RATIO = 53.33
    __RECT_INTERVAL_RATIO = 5.5
    __STARTING_Y_RATIO = 4.74
    __TOP_RECT_HEIGHT_RATIO = 7.83

    def __init__(self, pos):
        self.__pos = pos

    @property
    def top_rect_width(self):
        return self.__pos.width // 2 + 20

    @property
    def top_rect_height(self):
        return self.__pos.height // self.__TOP_RECT_HEIGHT_RATIO

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
