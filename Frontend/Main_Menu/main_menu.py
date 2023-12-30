from pygame import SRCALPHA, Surface
from Frontend.Helper_Files import WindowInterface, ButtonEventHandler
from Frontend.settings import DARK_PURPLE, WHITE
from .background import Background
from .Top import Top
from .Bottom import Bottom
from .Right import Right


class MainMenu(WindowInterface):
    __FONT_COLOR = WHITE
    __COLOR = DARK_PURPLE

    def __init__(self, display, window_manager, map_info, play_tracker):
        self.__display = display
        self.__pos = MainMenuPos(display=display)
        self.__main_menu_surface = Surface(self.__display.get_window_size, SRCALPHA)
        self.__top_div = Top(display=self.__display, map_info=map_info)
        self.__bottom_div = Bottom(display=self.__display)
        self.__right_div = Right(play_tracker=play_tracker, display=self.__display)
        self.__event_handler = ButtonEventHandler()
        self.__window_manager = window_manager
        self.__map_info = map_info
        self.__background = Background()
        self.__display.show_cursor()

    def run(self):
        self.__display.check_window_size()
        self.__background.show_background(window=self.__display.window, window_size=self.__display.get_window_size,
                                          map_background_status=self.__map_info.map_background_status)
        self.__top_div.show(main_menu_surface=self.__main_menu_surface)
        self.__bottom_div.show(main_menu_surface=self.__main_menu_surface)
        self.__right_div.show(main_menu_surface=self.__main_menu_surface)
        self.__display.window.blit(self.__main_menu_surface, (0, 0))


class MainMenuEventHandler:
    def __init__(self, main_menu: MainMenu, window_manager):
        self.__main_menu = main_menu
        self.__window_manager = window_manager

    def check_events(self):
        pass


class MainMenuPos:
    def __init__(self, display):
        self.__display = display
