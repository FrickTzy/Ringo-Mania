import pygame


class WindowManager:
    def __init__(self):
        self.__starting_screen, self.__main_menu, self.__play_window = None, None, None
        self.__current_window = None
        self.__running = True

    def add_window(self, main_menu, play_window):
        self.__main_menu = main_menu
        self.__play_window = play_window
        self.show_main_menu()

    @property
    def current_window(self):
        return self.__current_window

    def show_starting_screen(self):
        self.__current_window = self.__starting_screen

    def show_main_menu(self):
        self.__current_window = self.__main_menu

    def show_play_window(self):
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
