import pygame
from Backend import Music, Timer, MapManager, PlayTracker, MapInfo
from Frontend.Main_Menu import MainMenu
from Frontend.Mania_Window import ManiaPlayWindow
from Frontend.Helper_Files import Display, WindowManager
from Frontend.settings import FPS, BLACK, clock


class Main:
    __running = True

    def __init__(self):
        self.music = Music()
        self.timer = Timer()
        self.__display = Display()
        self.map_info = MapInfo(song_name="Torete")
        self.play_tracker = PlayTracker(self.map_info.song_name)
        self.__window_manager = WindowManager()
        self.__main_menu = MainMenu(display=self.__display, window_manager=self.__window_manager)
        self.__play_window = ManiaPlayWindow(music=self.music, timer=self.timer, map_manager=MapManager,
                                             play_tracker=self.play_tracker,
                                             map_info=self.map_info, display=self.__display,
                                             window_manager=self.__window_manager)
        self.__window_manager.add_window(main_menu=self.__main_menu, play_window=self.__play_window)

    def run(self):
        while self.__window_manager.running:
            self.update_frame()
            self.__window_manager.check_window_if_quit()
            self.__window_manager.current_window.run()
        pygame.quit()

    def update_frame(self):
        clock.tick(FPS)
        pygame.display.update()
        self.__display.window.fill(BLACK)


if __name__ == "__main__":
    main = Main()
    main.run()
