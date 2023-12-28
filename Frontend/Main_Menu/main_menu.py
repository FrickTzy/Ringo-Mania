from pygame import Rect, draw, SRCALPHA, Surface, font
from Frontend.Helper_Files import WindowInterface, ButtonEventHandler
from Frontend.settings import DARK_PURPLE


class MainMenu(WindowInterface):
    running = True

    def __init__(self, display, window_manager):
        self.__display = display
        self.__pos = MainMenuPos(display=display)
        self.__main_menu_surface = Surface(self.__display.get_window_size, SRCALPHA)
        self.__top_rect = Rect(0, 0, self.__display.width, 100)
        self.__bottom_rect = Rect(0, self.__display.height - 100, self.__display.width, 100)
        self.__event_handler = ButtonEventHandler()
        self.__font = ButtonFont()
        self.__window_manager = window_manager

    def run(self):
        draw.rect(self.__main_menu_surface, DARK_PURPLE, self.__top_rect)
        draw.rect(self.__main_menu_surface, DARK_PURPLE, self.__bottom_rect)
        self.__show_text()
        self.__display.window.blit(self.__main_menu_surface, (0, 0))

    def __show_text(self):
        text = self.__font.font.render("Mania", True, DARK_PURPLE)
        self.__main_menu_surface.blit(text, (300, 300))
        self.__event_handler.check_buttons_for_clicks(starting_pos=(300, 300),
                                                      text_size=self.__font.text_size(text="Mania"),
                                                      command=self.__window_manager.show_play_window)


class MainMenuPos:
    def __init__(self, display):
        self.__display = display

    @property
    def window_size(self):
        return self.__display.get_window_size


class ButtonFont:
    __FONT_RATIO = 23

    def __init__(self):
        self.font = font.SysFont("arialblack", 100)

    def text_size(self, text: str) -> tuple[int, int]:
        width, height = self.font.size(text)
        return width, height
