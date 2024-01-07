from pygame import SRCALPHA, Surface
from Frontend.Helper_Files import WindowInterface, State
from Frontend.Score_Screen import ScoreScreen
from Frontend.settings import DARK_PURPLE, WHITE
from .background import Background
from .Top import Top
from .Bottom import Bottom
from .Right import Right
from .Left import Left


class MainMenu(WindowInterface):
    __FONT_COLOR = WHITE
    __COLOR = DARK_PURPLE

    def __init__(self, display, window_manager, map_info, play_tracker):
        self.__display = display
        self.__pos = MainMenuPos(display=display)
        self.__event_handler = MainMenuEventHandler(main_menu=self, window_manager=window_manager)
        self.__main_menu_surface = Surface(self.__display.get_window_size, SRCALPHA)
        self.__top_div = Top(display=self.__display, map_info=map_info)
        self.__bottom_div = Bottom(display=self.__display)
        self.__right_div = Right(play_tracker=play_tracker, display=self.__display, state=self.__event_handler.state)
        self.__map_info = map_info
        self.__left_div = Left(display=self.__display, map_info=self.__map_info, state=self.__event_handler.state)
        self.__background = Background()
        self.__score_screen = ScoreScreen(window_size=self.__display.get_window_size, state=self.__event_handler.state,
                                          map_info=map_info)

    def run(self):
        self.__display.show_cursor()
        self.__display.check_window_size()
        self.__background.show_background(window=self.__display.window, window_size=self.__display.get_window_size,
                                          map_background_status=self.__map_info.map_background_status)
        self.__clear_surface()
        self.__left_div.show(main_menu_surface=self.__main_menu_surface)
        self.__top_div.show(main_menu_surface=self.__main_menu_surface)
        self.__bottom_div.show(main_menu_surface=self.__main_menu_surface)
        self.__right_div.show(main_menu_surface=self.__main_menu_surface, background_img=self.__background.background)
        self.__display.window.blit(self.__main_menu_surface, (0, 0))
        self.__event_handler.check_events()

    def __clear_surface(self):
        self.__main_menu_surface.fill((0, 0, 0, 0))

    def show_score_screen(self, play_stats: dict):
        self.__score_screen.show_score_screen(window=self.__display.window, stats=play_stats,
                                              size=self.__display.get_window_size,
                                              date_time={'date': play_stats['date'], 'time': play_stats['time']},
                                              grade=play_stats['grade'], has_delay=False)

    def hide_score_screen(self, play_stats: dict):
        self.__score_screen.hide_score_screen(window=self.__display.window, stats=play_stats,
                                              size=self.__display.get_window_size,
                                              date_time={'date': play_stats['date'], 'time': play_stats['time']},
                                              grade=play_stats['grade'], has_delay=False)

    def restart_score_screen(self):
        self.__score_screen.restart()


class MainMenuState(State):
    __show_score_screen = False
    __leave_main_menu = False
    __leave_score_screen = False
    __current_play: dict = {}

    def __init__(self):
        self.finished_fade_out = False

    def check_if_show_score_screen(self):
        return self.__show_score_screen

    @property
    def get_current_play(self):
        return self.__current_play

    def show_score_screen(self, current_play):
        self.__show_score_screen = True
        self.__current_play = current_play

    def leave_score_screen(self):
        self.__show_score_screen = False
        self.__leave_score_screen = True

    def reset_score_screen(self):
        self.__leave_score_screen = False

    def check_if_leave_score_screen(self):
        return self.__leave_score_screen


class MainMenuEventHandler:
    def __init__(self, main_menu: MainMenu, window_manager):
        self.__main_menu = main_menu
        self.__window_manager = window_manager
        self.__state = MainMenuState()

    @property
    def state(self):
        return self.__state

    def check_events(self):
        self.__check_if_show_score_screen()

    def __check_if_show_score_screen(self):
        if self.__state.check_if_show_score_screen():
            self.__main_menu.show_score_screen(play_stats=self.__state.get_current_play)
        if self.__state.check_if_leave_score_screen():
            self.__main_menu.hide_score_screen(play_stats=self.__state.get_current_play)
            if self.__state.finished_fade_out:
                self.__state.reset_score_screen()
                self.__main_menu.restart_score_screen()


class MainMenuPos:
    def __init__(self, display):
        self.__display = display
