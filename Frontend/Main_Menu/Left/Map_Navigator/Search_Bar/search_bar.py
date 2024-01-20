from pygame import font
from .search_tracker import SearchTracker
from Frontend.Settings import Color


class SearchBar:
    __COLOR = Color.DARK_PURPLE

    def __init__(self, search_tracker: SearchTracker, display):
        self.__tracker = search_tracker
        self.__pos = Pos(display=display)
        self.__font = Font()

    def show(self, surface):
        text = self.__font.font_object(height=self.__pos.height).render(f"{self.__tracker.current_search}", True,
                                                                        self.__COLOR)
        surface.blit(text, self.__pos.text_pos)


class Font:
    __MAP_MAKER_FONT_RATIO = 40

    def font_object(self, height):
        return font.SysFont("Arialblack", self.__font_size(height=height))

    def __font_size(self, height):
        return height // self.__MAP_MAKER_FONT_RATIO


class Pos:
    def __init__(self, display):
        self.__display = display

    @property
    def height(self):
        return self.__display.height

    @property
    def text_pos(self):
        return 100, 200

    @property
    def get_window_size(self):
        return self.__display.get_window_size
