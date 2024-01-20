from pygame import Rect, draw
from .top_rect_text import TopRectText
from .play_time_text import PlayTimeText
from Frontend.Settings import Color


class TopRect:
    __COLOR = Color.DARK_PURPLE

    def __init__(self, pos, map_info):
        self.__pos = TopRectPos(pos=pos)
        self.__rect = Rect(self.__pos.x, 0, self.__pos.width, self.__pos.height)
        self.__text = TopRectText(pos=pos)
        self.__time = PlayTimeText(pos=pos)
        self.__map_info = map_info

    def show(self, screen, date_time: dict):
        self.__update_rect()
        draw.rect(screen, self.__COLOR, self.__rect)
        self.__text.show_text(screen=screen, song_info=self.__map_info.song_info,
                              map_maker=self.__map_info.map_maker)
        self.__time.show(screen=screen, date_time=date_time)

    def __update_rect(self):
        self.__rect = Rect(self.__pos.x, 0, self.__pos.width, self.__pos.height)


class TopRectPos:
    __HEIGHT_RATIO = 5.5
    __X_PADDING_RATIO = 160

    def __init__(self, pos):
        self.__pos = pos

    @property
    def height(self):
        return self.__pos.height // self.__HEIGHT_RATIO

    @property
    def width(self):
        return self.__pos.width // 2

    @property
    def x(self):
        return (self.__pos.width // 2) + self.__x_padding

    @property
    def __x_padding(self):
        return self.__pos.width // self.__X_PADDING_RATIO
