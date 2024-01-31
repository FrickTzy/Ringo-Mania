from pygame import font
from Frontend.Settings import Color
from Frontend.Helper_Files import ButtonEventHandler


class Text:
    __COLOR = Color.WHITE

    def __init__(self, map_info, display):
        self.__map_info = map_info
        self.__event_handler = ButtonEventHandler()
        self.__font = Font()
        self.__pos = TextPos(display=display)

    def show_text(self, surface):
        self.__font.check_if_update_font(height=self.__pos.height)
        self.__show_song_name(surface=surface)
        self.__show_song_artist(surface=surface)

    def __show_song_name(self, surface):
        unfiltered_name: str = self.__map_info.song_file_name
        song_name = self.__check_song_text_conditions(song_name=unfiltered_name,
                                                      text_width=self.__font.text_width(text=unfiltered_name))
        song_name_font = self.__font.font.render(song_name, True,
                                                 self.__COLOR)
        surface.blit(song_name_font, self.__pos.song_pos)

    @staticmethod
    def __check_song_text_conditions(song_name: str, text_width) -> str:
        if text_width > 700:
            if "-" in song_name:
                index = song_name.index("-")
                return song_name[index + 2::]
        return song_name

    def __show_song_artist(self, surface):
        artist = self.__font.font.render(f"Song by {self.__map_info.song_artist}", True,
                                         self.__COLOR)
        surface.blit(artist, self.__pos.artist_pos)


class Font:
    __FONT_RATIO = 26.67
    __current_height = 0

    def __init__(self):
        self.__font = font.SysFont("arialblack", 30)

    @property
    def font(self):
        return self.__font

    def __update_font(self, height) -> None:
        self.__font = font.SysFont("arialblack", self.__font_size(height=height))

    def check_if_update_font(self, height):
        if self.__current_height == height:
            return
        self.__update_font(height=height)
        self.__current_height = height

    def __font_size(self, height):
        return int(height // self.__FONT_RATIO)

    def text_size(self, text: str) -> tuple[int, int]:
        width, height = self.__font.size(text)
        return width, height

    def text_width(self, text: str):
        return self.text_size(text=text)[0]


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
