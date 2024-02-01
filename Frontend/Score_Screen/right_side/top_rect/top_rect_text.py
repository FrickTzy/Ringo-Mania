from pygame import font
from Frontend.Settings import Color


class TopRectText:
    __COLOR = Color.WHITE

    def __init__(self, pos):
        self.__font = Font()
        self.__pos = TextPos(pos=pos)

    def show_text(self, screen, song_info: str, map_maker: str):
        self.__font.check_if_update_font(height=self.__pos.height, text=song_info)
        song_info_text, map_maker_text = self.__render_text(song_info=song_info, map_maker=map_maker)
        self.__blit_text(screen=screen, song_info_text=song_info_text, map_maker_text=map_maker_text)

    def __render_text(self, song_info: str, map_maker: str):
        song_info_text = self.__font.song_info_font.render(song_info, True, self.__COLOR)
        map_maker_text = self.__font.map_maker_font.render(f"Beatmap by {map_maker}", True, self.__COLOR)
        return song_info_text, map_maker_text

    def __blit_text(self, screen, song_info_text, map_maker_text):
        screen.blit(song_info_text, self.__pos.song_info_pos)
        screen.blit(map_maker_text, self.__pos.map_maker_pos)


class Font:
    __SONG_FONT_RATIO = 21
    __MAP_MAKER_FONT_RATIO = 34
    __FONT_SIZE_CAP = 40
    __current_text = ""
    __current_height = 0

    def __init__(self):
        self.__song_info_font = font.SysFont("Arialblack", 20)
        self.__map_maker_font = font.SysFont("Arialblack", 15)

    @property
    def song_info_font(self):
        return self.__song_info_font

    @property
    def map_maker_font(self):
        return self.__map_maker_font

    def __update_song_info_font(self, height: int, text: str):
        self.__song_info_font = font.SysFont("Arialblack", self.__song_font_size(height=height, text=text))
        if self.__song_info_width(text=text) + 870 >= 1550:
            self.__song_info_font = font.SysFont("Arialblack", self.__FONT_SIZE_CAP)

    def __update_map_maker_font(self, height: int):
        self.__map_maker_font = font.SysFont("Arialblack", self.__map_maker_font_size(height=height))

    def __update_font(self, height: int, text: str):
        self.__update_song_info_font(height=height, text=text)
        self.__update_map_maker_font(height=height)

    def check_if_update_font(self, height: int, text: str):
        if self.__current_height == height and self.__current_text == text:
            return
        self.__update_font(height=height, text=text)
        self.__current_height, self.__current_text = height, text

    def __song_font_size(self, height: int, text):
        return height // self.__SONG_FONT_RATIO

    def __map_maker_font_size(self, height: int):
        return height // self.__MAP_MAKER_FONT_RATIO

    def __song_info_width(self, text: str) -> int:
        width, height = self.__song_info_font.size(text)
        return width


class TextPos:
    __TEXT_X_RATIO = 1.84
    __SONG_INFO_Y_RATIO = 60
    __MAP_MAKER_Y_RATIO = 13

    def __init__(self, pos):
        self.__pos = pos

    @property
    def song_info_pos(self):
        return self.__text_x, self.__song_info_y

    @property
    def map_maker_pos(self):
        return self.__text_x, self.__map_maker_y

    @property
    def __text_x(self):
        return self.__pos.width // self.__TEXT_X_RATIO

    @property
    def __song_info_y(self):
        return self.__pos.height // self.__SONG_INFO_Y_RATIO

    @property
    def __map_maker_y(self):
        return self.__pos.height // self.__MAP_MAKER_Y_RATIO

    @property
    def height(self):
        return self.__pos.height
