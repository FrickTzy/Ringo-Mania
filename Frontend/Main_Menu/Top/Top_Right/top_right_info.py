from pygame import Rect, draw
from Frontend.settings import DARK_PURPLE
from Frontend.Main_Menu.Top.Top_Right.top_right_text import Text


class TopRight:
    __COLOR = DARK_PURPLE

    def __init__(self, display, map_info, outline):
        self.__pos = Pos(display=display)
        self.__text = Text(map_info=map_info, display=display)
        self.__outline = outline
        self.__top_right_rect = Rect(self.__pos.x, 0, self.__pos.width, self.__pos.top_rect_height)

    def __update_rect(self):
        self.__top_right_rect = Rect(self.__pos.x, 0, self.__pos.width, self.__pos.top_rect_height)

    def show(self, main_menu_surface):
        self.__update_rect()
        self.__show_rect(main_menu_surface=main_menu_surface)
        self.__text.show_text(main_menu_surface=main_menu_surface)

    def __show_rect(self, main_menu_surface):
        self.__outline.show_outline(main_menu_surface=main_menu_surface, rect=self.__top_right_rect)
        draw.rect(main_menu_surface, self.__COLOR, self.__top_right_rect)


class Pos:
    __HEIGHT_RATIO = 5.80

    def __init__(self, display):
        self.__display = display

    @property
    def width(self):
        return self.__display.width // 2

    @property
    def x(self):
        return self.__display.width // 2

    @property
    def top_rect_height(self):
        return self.__display.height // self.__HEIGHT_RATIO
