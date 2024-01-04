from pygame import Rect, draw
from Frontend.settings import DARK_PURPLE, PURPLE
from Frontend.Main_Menu.Top.Top_Right.top_right_info import TopRight


class Top:
    __COLOR = DARK_PURPLE

    def __init__(self, display, map_info):
        self.__pos = Pos(display=display)
        self.__top_rect = Rect(0, 0, self.__pos.width, self.__pos.top_rect_height)
        self.__outline = Outline()
        self.__top_right_div = TopRight(display=display, map_info=map_info, outline=self.__outline)

    def __update_rect(self):
        self.__top_rect = Rect(0, 0, self.__pos.width, self.__pos.top_rect_height)

    def show(self, main_menu_surface):
        self.__update_rect()
        self.__top_right_div.show(main_menu_surface=main_menu_surface)
        self.__show_rect(main_menu_surface=main_menu_surface)

    def __show_rect(self, main_menu_surface):
        self.__outline.show_outline(main_menu_surface=main_menu_surface, rect=self.__top_rect)
        draw.rect(main_menu_surface, self.__COLOR, self.__top_rect)


class Pos:
    __HEIGHT_RATIO = 8

    def __init__(self, display):
        self.__display = display

    @property
    def width(self):
        return self.__display.width // 2

    @property
    def top_rect_height(self):
        return self.__display.height // self.__HEIGHT_RATIO


class Outline:
    __OUTLINE_COLOR = PURPLE
    __OUTLINE_OPACITY = 80
    __OUTLINE_THICKNESS = 10

    def show_outline(self, main_menu_surface, rect: Rect):
        outline = Rect(rect.x - self.__OUTLINE_THICKNESS, self.__OUTLINE_THICKNESS,
                       rect.width + self.__OUTLINE_THICKNESS,
                       rect.height)
        r, g, b = self.__OUTLINE_COLOR
        draw.rect(main_menu_surface, (r, g, b, self.__OUTLINE_OPACITY), outline)
