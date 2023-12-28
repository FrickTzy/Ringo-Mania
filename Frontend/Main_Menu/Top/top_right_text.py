from pygame import font
from Frontend.settings import WHITE
from Frontend.Helper_Files import ButtonEventHandler


class Text:
    __COLOR = WHITE

    def __init__(self, map_info, display):
        self.__map_info = map_info
        self.__event_handler = ButtonEventHandler()
        self.__font = Font()
        self.__pos = TextPos(display=display)

    def show_text(self, main_menu_surface):
        song_name = self.__font.font(height=self.__pos.height).render(self.__map_info.song_file_name, True,
                                                                      self.__COLOR)
        artist = self.__font.font(height=self.__pos.height).render(f"Song by {self.__map_info.song_artist}", True,
                                                                   self.__COLOR)
        main_menu_surface.blit(song_name, self.__pos.song_pos)
        main_menu_surface.blit(artist, self.__pos.artist_pos)
        """self.__event_handler.check_buttons_for_clicks(starting_pos=self.__pos.text_pos,
                                                      text_size=self.__font.text_size(text="Mania"),
                                                      command=self.__window_manager.show_play_window)"""


class Font:
    __FONT_RATIO = 26.67

    def __init__(self):
        self.__font = font.SysFont("arialblack", 30)

    def font(self, height):
        self.__font = font.SysFont("arialblack", self.__font_size(height=height))
        return self.__font

    def __font_size(self, height):
        return int(height // self.__FONT_RATIO)

    def text_size(self, text: str) -> tuple[int, int]:
        width, height = self.__font.size(text)
        return width, height


class TextPos:
    __X_RATIO = 1.89
    __SONG_NAME_RATIO, __SONG_ARTIST_RATIO = 40, 11.43

    def __init__(self, display):
        self.__display = display

    @property
    def __x(self):
        return self.__display.width // self.__X_RATIO

    @property
    def __song_y(self):
        return self.__display.height // self.__SONG_NAME_RATIO

    @property
    def __artist_y(self):
        return self.__display.height // self.__SONG_ARTIST_RATIO

    @property
    def song_pos(self):
        return self.__x, self.__song_y

    @property
    def artist_pos(self):
        return self.__x, self.__artist_y

    @property
    def height(self):
        return self.__display.height
