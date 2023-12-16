from pygame import Rect, draw
from .top_rect_text import TopRectText
from Frontend.settings import DARK_PURPLE


class TopRect:
    __COLOR = DARK_PURPLE

    def __init__(self, pos, map_info):
        self.__pos = TopRectPos(pos=pos)
        self.__rect = Rect(self.__pos.x, 0, self.__pos.width, self.__pos.height)
        self.__text = TopRectText(pos=pos)
        self.__map_info = map_info

    def show(self, end_screen):
        draw.rect(end_screen, DARK_PURPLE, self.__rect)
        self.__text.show_text(end_screen=end_screen, song_info=self.__map_info.song_info,
                              map_maker=self.__map_info.map_maker)


class TopRectPos:
    __HEIGHT_RATIO = 6.2

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
        return (self.__pos.width // 2) + 10
