from pygame import font
from Frontend.settings import WHITE


class TopRectText:
    __COLOR = WHITE

    def __init__(self, pos):
        self.__font = Font()
        self.__pos = TextPos(pos=pos)

    def show_text(self, end_screen, song_info: str, map_maker: str):
        song_info_text = self.__font.song_info_font(height=self.__pos.height, text=song_info).render(song_info, True,
                                                                                                     self.__COLOR)
        map_maker_text = self.__font.map_maker_font(height=self.__pos.height).render(f"Beatmap by {map_maker}", True,
                                                                                     self.__COLOR)
        end_screen.blit(song_info_text, self.__pos.song_info_pos)
        end_screen.blit(map_maker_text, self.__pos.map_maker_pos)


class Font:
    __SONG_FONT_RATIO = 19
    __ARTIST_FONT_RATIO = 32
    __FONT_SIZE_CAP = 40

    def __init__(self):
        self.__song_info_font = font.SysFont("Arialblack", 20)
        self.__map_maker_font = font.SysFont("Arialblack", 15)

    def song_info_font(self, height: int, text: str):
        self.__song_info_font = font.SysFont("Arialblack", self.__song_font_size(height=height, text=text))
        if self.__song_info_width(text=text) + 870 >= 1550:
            self.__song_info_font = font.SysFont("Arialblack", self.__FONT_SIZE_CAP)
        return self.__song_info_font

    def map_maker_font(self, height: int):
        self.__map_maker_font = font.SysFont("Arialblack", self.__song_artist_size(height=height))
        return self.__map_maker_font

    def __song_font_size(self, height: int, text):
        return height // self.__SONG_FONT_RATIO

    def __song_artist_size(self, height: int):
        return height // self.__ARTIST_FONT_RATIO

    def __song_info_width(self, text: str) -> int:
        width, height = self.__song_info_font.size(text)
        return width


class TextPos:
    def __init__(self, pos):
        self.__pos = pos

    @property
    def song_info_pos(self):
        return 870, 15

    @property
    def map_maker_pos(self):
        return 870, 75

    @property
    def height(self):
        return self.__pos.height
