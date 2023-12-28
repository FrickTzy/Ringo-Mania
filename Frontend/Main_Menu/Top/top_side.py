from pygame import Rect, draw
from Frontend.settings import DARK_PURPLE
from .top_right_info import TopRight


class Top:
    __COLOR = DARK_PURPLE

    def __init__(self, display, map_info):
        self.__pos = Pos(display=display)
        self.__top_rect = Rect(0, 0, self.__pos.width, self.__pos.top_rect_height)
        self.__top_right_div = TopRight(display=display, map_info=map_info)

    def __update_rect(self):
        self.__top_rect = Rect(0, 0, self.__pos.width, self.__pos.top_rect_height)

    def show(self, main_menu_surface):
        self.__update_rect()
        draw.rect(main_menu_surface, self.__COLOR, self.__top_rect)
        self.__top_right_div.show(main_menu_surface=main_menu_surface)


class Pos:
    __HEIGHT_RATIO = 8

    def __init__(self, display):
        self.__display = display

    @property
    def width(self):
        return self.__display.width

    @property
    def top_rect_height(self):
        return self.__display.height // self.__HEIGHT_RATIO
