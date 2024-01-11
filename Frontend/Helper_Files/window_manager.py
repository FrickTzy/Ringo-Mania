import pygame
from Frontend.Helper_Files.Transition.fade_effect import FadeEffect


class WindowManager:
    __running = True

    def __init__(self, display):
        self.__starting_screen, self.__main_menu, self.__play_window = None, None, None
        self.__current_window = None
        self.__transition = Transition(display=display)

    def add_window(self, main_menu, play_window):
        self.__main_menu = main_menu
        self.__play_window = play_window
        self.show_main_menu()

    @property
    def current_window(self):
        return self.__current_window

    def run_current_window(self):
        self.__current_window.run()
        self.__transition.check_for_transition()

    def show_starting_screen(self):
        self.__current_window = self.__starting_screen

    def show_main_menu(self):
        self.__main_menu.reset_all()
        if self.__current_window is None:
            self.__current_window = self.__main_menu
            return
        self.__transition.start_transition()
        if self.__transition.finish_fading_in:
            self.__current_window = self.__main_menu

    def show_play_window(self):
        self.__play_window.restart()
        self.__current_window = self.__play_window

    def quit(self):
        self.__running = False

    @property
    def running(self):
        return self.__running

    def check_window_if_quit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()


class Transition:
    __start_transition = False

    def __init__(self, display):
        self.__transition = FadeEffect(pos=display)
        self.__display = display
        self.__transition_surface = pygame.Surface(self.__display.get_window_size, pygame.SRCALPHA)

    def check_for_transition(self):
        if not self.__start_transition:
            return
        if self.__transition.finished_fading_out:
            self.__start_transition = False
            self.__transition.reset()
            return
        self.__show_transition()

    def __update_surface(self):
        self.__transition_surface = pygame.Surface(self.__display.get_window_size, pygame.SRCALPHA)

    def __show_transition(self):
        self.__update_surface()
        self.__transition.show(window=self.__display.window, screen=self.__transition_surface)
        if self.__transition.halfway_fade_out:
            self.__display.show_cursor()

    def start_transition(self):
        self.__start_transition = True

    @property
    def finish_fading_in(self):
        return self.__transition.finished_fade_in
