from pygame import SRCALPHA, Surface, QUIT, KEYDOWN, MOUSEWHEEL, event as pyevent
from Frontend.Helper_Files import WindowInterface, State
from Frontend.Helper_Files.Interfaces import WindowEventHandler
from Frontend.Score_Screen import ScoreScreen
from Frontend.Settings import Color
from .background import Background
from .Top import Top
from .Bottom import Bottom
from .Right import Right
from .Left import Left
from .Left.Map_Navigator.Search_Bar import SearchTracker


class MainMenu(WindowInterface):
    __FONT_COLOR = Color.WHITE
    __COLOR = Color.DARK_PURPLE

    def __init__(self, display, window_manager, map_info, play_tracker, music):
        self.__display = display
        self.__pos = MainMenuPos(display=display)
        self.__music = music
        self.__search_tracker = SearchTracker()
        self.__notifier = EventHandlerNotifier()
        self.__event_handler = MainMenuEventHandler(main_menu=self, window_manager=window_manager,
                                                    search_tracker=self.__search_tracker, notifier=self.__notifier)
        self.__main_menu_surface = Surface(self.__display.get_window_size, SRCALPHA)
        self.__top_div = Top(display=self.__display, map_info=map_info)
        self.__bottom_div = Bottom(display=self.__display)
        self.__right_div = Right(play_tracker=play_tracker, display=self.__display, state=self.__event_handler.state)
        self.__map_info = map_info
        self.__left_div = Left(display=self.__display, map_info=self.__map_info, state=self.__event_handler.state,
                               search_tracker=self.__search_tracker, notifier=self.__notifier)
        self.__background = Background()
        self.__score_screen = ScoreScreen(window_size=self.__display.get_window_size, state=self.__event_handler.state,
                                          map_info=map_info)

    def run(self):
        self.__setup()
        self.__show()
        self.__blit()
        self.__event_handler.check_events()
        self.__check_if_changed_map()

    def __setup(self):
        self.__display.show_cursor()
        self.__display.check_window_size()
        self.__clear_surface()
        self.__music.check_if_repeat()

    def __blit(self):
        self.__display.window.blit(self.__main_menu_surface, (0, 0))

    def __show(self):
        self.__left_div.show(main_menu_surface=self.__main_menu_surface)
        self.__top_div.show(main_menu_surface=self.__main_menu_surface)
        self.__bottom_div.show(main_menu_surface=self.__main_menu_surface)
        self.__background.show_background(window=self.__display.window,
                                          image=self.__map_info.current_background_image)
        self.__right_div.show(main_menu_surface=self.__main_menu_surface, background_img=self.__background.background)

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

    def __check_if_changed_map(self):
        if self.__map_info.changed:
            self.__music.play_music()
            self.__right_div.restart()
        self.__map_info.changed = False

    def reset_all(self):
        self.__music.reset_volume()
        self.__music.stop_music()
        self.__map_info.changed = True
        self.__left_div.update()
        self.__event_handler.reset_all()


class MainMenuState(State):
    __show_score_screen = False
    __leave_main_menu = False
    __leave_score_screen = False
    __show_play_window = False
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

    def show_play_window(self):
        self.__show_play_window = True

    def reset_play_window(self):
        self.__show_play_window = False

    @property
    def check_if_show_play_window(self):
        return self.__show_play_window

    def reset_all(self):
        self.reset_play_window()
        self.reset_score_screen()


class MainMenuEventHandler(WindowEventHandler):
    def __init__(self, main_menu: MainMenu, window_manager, search_tracker: SearchTracker,
                 notifier):
        self.__main_menu = main_menu
        self.__window_manager = window_manager
        self.__state = MainMenuState()
        self.__search_tracker = search_tracker
        self.__notifier = notifier

    @property
    def state(self):
        return self.__state

    def check_events(self):
        self.check_window_if_quit()
        self.__check_if_show_score_screen()
        self.__check_if_show_play_window()

    def reset_all(self):
        self.__state.reset_all()

    def __check_if_show_score_screen(self):
        if self.__state.check_if_show_score_screen():
            self.__main_menu.show_score_screen(play_stats=self.__state.get_current_play)
        if self.__state.check_if_leave_score_screen():
            self.__main_menu.hide_score_screen(play_stats=self.__state.get_current_play)
            if self.__state.finished_fade_out:
                self.__state.reset_score_screen()
                self.__main_menu.restart_score_screen()

    def __check_if_show_play_window(self):
        if self.__state.check_if_show_play_window:
            self.__window_manager.show_play_window()

    def check_window_if_quit(self):
        for event_occurrence in pyevent.get():
            self.__check_if_key_down(event_occurrence=event_occurrence)
            self.__check_if_scroll(event_occurrence=event_occurrence)
            self.__check_if_quit(event_occurrence=event_occurrence)

    def __check_if_key_down(self, event_occurrence):
        if event_occurrence.type == KEYDOWN:
            self.__search_tracker.add_letter(event=event_occurrence)

    def __check_if_quit(self, event_occurrence):
        if event_occurrence.type == QUIT:
            self.__window_manager.quit()

    def __check_if_scroll(self, event_occurrence):
        if event_occurrence.type == MOUSEWHEEL:
            self.__notifier.set_scroll()
            self.__notifier.set_event(event=event_occurrence)


class EventHandlerNotifier:
    __scrolled = False
    __event = None

    @property
    def scrolled(self):
        scrolled = self.__scrolled
        self.__scrolled = False
        return scrolled

    @property
    def event(self):
        return self.__event

    def set_scroll(self):
        self.__scrolled = True

    def set_event(self, event):
        self.__event = event


class MainMenuPos:
    def __init__(self, display):
        self.__display = display
