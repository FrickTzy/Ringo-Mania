from pygame import font
from .search_tracker import SearchTracker
from Frontend.Settings import Color
from Frontend.Helper_Files import ButtonEventHandler


class SearchBar:
    __COLOR = Color.DARK_PURPLE
    __SECONDARY_COLOR = Color.WHITE
    __EMPTY_SEARCH_OPACITY = 100
    __current_text = ""

    def __init__(self, search_tracker: SearchTracker, display):
        self.__tracker = search_tracker
        self.__pos = Pos(display=display)
        self.__font = Font()
        self.__button_event_handler = ButtonEventHandler()

    def show(self, surface, selected_map_bar_pos: tuple, map_bar_size: tuple):
        current_search = self.__tracker.current_search
        self.__update_text(current_search=current_search)
        text = self.__font.render(text=self.__current_text,
                                  color=self.__color(selected_map_bar_pos=selected_map_bar_pos,
                                                     map_bar_size=map_bar_size))
        self.__check_if_change_opacity(text=text, current_search=current_search)
        surface.blit(text, self.__pos.text_pos)

    def __color(self, selected_map_bar_pos: tuple, map_bar_size: tuple):
        if self.__text_overlaying_selected_map_bar(selected_map_bar_pos=selected_map_bar_pos,
                                                   map_bar_size=map_bar_size):
            return self.__SECONDARY_COLOR
        return self.__COLOR

    def __update_text(self, current_search):
        self.__font.check_if_update_font(height=self.__pos.height)
        self.__set_current_text(current_search=current_search)

    def __set_current_text(self, current_search):
        self.__current_text = f"Search: {current_search}"

    def __text_overlaying_selected_map_bar(self, selected_map_bar_pos: tuple, map_bar_size: tuple) -> bool:
        if self.__button_event_handler. \
                check_if_an_object_collides_with_another_object(starting_pos_1=selected_map_bar_pos,
                                                                size_1=map_bar_size,
                                                                starting_pos_2=self.__pos.text_pos,
                                                                size_2=self.__font.get_font_size(
                                                                    text=self.__current_text)):
            return True
        return False

    def __check_if_change_opacity(self, text, current_search):
        if not current_search:
            text.set_alpha(self.__EMPTY_SEARCH_OPACITY)


class Font:
    __MAP_MAKER_FONT_RATIO = 49
    __current_height = 0

    def __init__(self):
        self.__font = font.SysFont("Arialblack", 20)

    def check_if_update_font(self, height) -> None:
        if self.__current_height == height:
            return
        self.__update_font(height=height)
        self.__current_height = height

    def __update_font(self, height) -> None:
        self.__font = font.SysFont("Arialblack", self.__font_size(height=height))

    @property
    def font(self):
        return self.__font

    def get_font_size(self, text: str):
        return self.__font.size(text)

    def __font_size(self, height):
        return height // self.__MAP_MAKER_FONT_RATIO

    def render(self, text, color):
        return self.__font.render(text, True, color)


class Pos:
    def __init__(self, display):
        self.__display = display

    @property
    def height(self):
        return self.__display.height

    @property
    def text_pos(self):
        return 30, 135

    @property
    def get_window_size(self):
        return self.__display.get_window_size
