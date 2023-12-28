from pygame import Rect, draw
from Frontend.settings import DARK_PURPLE


class Bottom:
    __COLOR = DARK_PURPLE

    def __init__(self, display):
        self.__pos = Pos(display=display)
        self.__bottom_rect = Rect(0, self.__pos.y, self.__pos.width, self.__pos.bottom_rect_height)

    def __update_rect(self):
        self.__bottom_rect = Rect(0, self.__pos.y, self.__pos.width, self.__pos.bottom_rect_height)

    def show(self, main_menu_surface):
        self.__update_rect()
        draw.rect(main_menu_surface, self.__COLOR, self.__bottom_rect)


class Pos:
    __HEIGHT_RATIO = 8

    def __init__(self, display):
        self.__display = display

    @property
    def width(self):
        return self.__display.width

    @property
    def y(self):
        return self.__display.height - self.bottom_rect_height

    @property
    def bottom_rect_height(self):
        return self.__display.height // self.__HEIGHT_RATIO
