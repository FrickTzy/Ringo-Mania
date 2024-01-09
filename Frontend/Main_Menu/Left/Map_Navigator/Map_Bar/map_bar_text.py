from pygame import font
from Frontend.settings import WHITE


class MapBarText:
    __COLOR = WHITE
    __BLUR_OPACITY = 140

    def __init__(self, map_info, pos):
        self.__font = Font()
        self.__pos = TextPos(pos=pos)
        self.__map_info = map_info

    def show_text(self, main_menu_surface, is_chosen: bool):
        self.__show_song_name_text(main_menu_surface=main_menu_surface, is_chosen=is_chosen)
        self.__show_song_artist_text(main_menu_surface=main_menu_surface, is_chosen=is_chosen)

    def __show_song_name_text(self, main_menu_surface, is_chosen: bool = False):
        song_name = self.__map_info.song_name.removesuffix(".mp3")
        song_name_text = self.__font.song_font(height=self.__pos.height).render(song_name,
                                                                                True, self.__COLOR)
        self.__check_if_blur(text_object=song_name_text, not_blur=is_chosen)
        if is_chosen:
            main_menu_surface.blit(song_name_text,
                                   self.__pos.song_name_pos(text_width=self.__font.song_text_width(text=song_name),
                                                            is_chosen=is_chosen))
        else:
            main_menu_surface.blit(song_name_text,
                                   self.__pos.song_name_pos(text_width=self.__font.song_text_width(text=song_name),
                                                            is_chosen=is_chosen))

    def __show_song_artist_text(self, main_menu_surface, is_chosen: bool = False):
        song_artist = self.__map_info.song_artist
        song_artist_text = self.__font.artist_font(height=self.__pos.height).render(song_artist,
                                                                                    True, self.__COLOR)
        self.__check_if_blur(text_object=song_artist_text, not_blur=is_chosen)
        if is_chosen:
            main_menu_surface.blit(song_artist_text,
                                   self.__pos.song_artist_pos(
                                       text_width=self.__font.artist_text_width(text=song_artist), is_chosen=is_chosen))
        else:
            main_menu_surface.blit(song_artist_text,
                                   self.__pos.song_artist_pos(
                                       text_width=self.__font.artist_text_width(text=song_artist), is_chosen=is_chosen))

    def __check_if_blur(self, text_object, not_blur: bool):
        if not_blur:
            text_object.set_alpha(255)
        else:
            text_object.set_alpha(self.__BLUR_OPACITY)


class Font:
    __SONG_FONT_RATIO = 43
    __ARTIST_FONT_RATIO = 60

    def __init__(self):
        self.__song_font = font.SysFont("arialblack", 30)
        self.__artist_font = font.SysFont("arialblack", 20)

    def song_font(self, height):
        self.__song_font = font.SysFont("arialblack", self.__song_font_size(height=height))
        return self.__song_font

    def artist_font(self, height):
        self.__artist_font = font.SysFont("arialblack", self.__artist_font_size(height=height))
        return self.__artist_font

    def __song_font_size(self, height):
        return int(height // self.__SONG_FONT_RATIO)

    def __artist_font_size(self, height):
        return int(height // self.__ARTIST_FONT_RATIO)

    def song_text_size(self, text: str) -> tuple[int, int]:
        width, height = self.__song_font.size(text)
        return width, height

    def song_text_width(self, text: str) -> int:
        return self.__song_font.size(text)[0]

    def artist_text_width(self, text: str) -> int:
        return self.__artist_font.size(text)[0]


class TextPos:
    __X_RATIO = 1.89
    __SONG_NAME_RATIO, __SONG_ARTIST_RATIO = 40, 11.43

    def __init__(self, pos):
        self.__pos = pos

    @property
    def height(self):
        return self.__pos.height

    def song_name_pos(self, text_width, is_chosen: bool = False):
        if is_chosen:
            return 620 - text_width, self.__pos.record_y + 10
        return 540 - text_width, self.__pos.record_y + 10

    def song_artist_pos(self, text_width, is_chosen: bool = False):
        if is_chosen:
            return 620 - text_width, self.__pos.record_y + 35
        return 540 - text_width, self.__pos.record_y + 35
