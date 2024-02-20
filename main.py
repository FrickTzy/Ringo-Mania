import pygame
from Backend import Music, Timer, MapManager, PlayTracker, MapInfo, ProfileImageManager
from Frontend.Main_Menu import MainMenu
from Frontend.Mania_Window import ManiaPlayWindow
from Frontend.Helper_Files import Display, WindowManager
from Frontend.Settings import Color, FPS


class Main:
    __CLOCK = pygame.time.Clock()
    __FRAME_COLOR = Color.BLACK

    def __init__(self):
        self.__timer = Timer()
        self.__display = Display()
        self.__map_info = MapInfo()
        self.__music = Music(map_info=self.__map_info)
        self.__play_tracker = PlayTracker(map_info=self.__map_info)
        self.__window_manager = WindowManager(display=self.__display)
        self.__main_menu = MainMenu(display=self.__display, window_manager=self.__window_manager,
                                    map_info=self.__map_info, play_tracker=self.__play_tracker, music=self.__music,
                                    profile_image_manager=ProfileImageManager())
        self.__play_window = ManiaPlayWindow(music=self.__music, timer=self.__timer, map_manager=MapManager,
                                             play_tracker=self.__play_tracker,
                                             map_info=self.__map_info, display=self.__display,
                                             window_manager=self.__window_manager)
        self.__window_manager.add_window(main_menu=self.__main_menu, play_window=self.__play_window)

    def run(self):
        while self.__window_manager.running:
            self.__update_frame()
            self.__window_manager.run_current_window()
        pygame.quit()

    def __update_frame(self):
        self.__CLOCK.tick(FPS)
        pygame.display.update()
        self.__display.window.fill(self.__FRAME_COLOR)


if __name__ == "__main__":
    main = Main()
    main.run()
