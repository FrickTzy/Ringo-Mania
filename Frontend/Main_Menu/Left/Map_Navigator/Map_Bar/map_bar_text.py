from pygame import font
from Frontend.settings import WHITE


class MapBarText:
    __COLOR = WHITE

    def __init__(self, map_info, pos):
        self.__font = Font()
        self.__pos = TextPos(pos=pos)
        self.__map_info = map_info

    def show_text(self, main_menu_surface):
        song_name = self.__map_info.song_name.removesuffix(".mp3")
        song_name_text = self.__font.font(height=self.__pos.height).render(song_name,
                                                                           True, self.__COLOR)
        main_menu_surface.blit(song_name_text,
                               self.__pos.song_name_pos(text_width=self.__font.text_width(text=song_name)))


class Font:
    __FONT_RATIO = 43

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

    def text_width(self, text: str) -> int:
        return self.__font.size(text)[0]


class TextPos:
    __X_RATIO = 1.89
    __SONG_NAME_RATIO, __SONG_ARTIST_RATIO = 40, 11.43

    def __init__(self, pos):
        self.__pos = pos

    @property
    def height(self):
        return self.__pos.height

    def song_name_pos(self, text_width):
        return 540 - text_width, self.__pos.record_y + 10
