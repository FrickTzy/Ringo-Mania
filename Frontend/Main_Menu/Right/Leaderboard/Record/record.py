from pygame import Rect, draw, image, transform
from os import path
from .text_stat import TextStats
from Frontend.settings import DARK_PURPLE, PLAYER_NAME


class Record:
    __COLOR = DARK_PURPLE
    __OPACITY = 210

    def __init__(self, play_dict, display):
        self.__pos = RecordPos(display=display)
        self.__text_stats = TextStats(play_info=play_dict, pos=self.__pos)
        self.__rect = Rect(0, 0, self.__pos.record_width, self.__pos.record_height)
        self.__profile = RecordProfile(pos=self.__pos)

    def show(self, main_menu_surface, y: int):
        self.__update_rect(y=y)
        self.__draw_rect(main_menu_surface=main_menu_surface)
        self.__profile.show_profile(main_menu_surface=main_menu_surface)
        self.__text_stats.show_text(main_menu_surface=main_menu_surface)

    def __draw_rect(self, main_menu_surface):
        r, g, b = self.__COLOR
        draw.rect(main_menu_surface, (r, g, b, self.__OPACITY), self.__rect)

    def __update_rect(self, y: int):
        self.__pos.set_record_y(padding=y)
        self.__rect = Rect(self.__pos.record_x, self.__pos.record_y, self.__pos.record_width,
                           self.__pos.record_height)


class RecordProfile:
    def __init__(self, pos):
        self.__pos = ProfilePos(pos=pos)
        self.__profile = image.load(path.join("Frontend\Main_Menu\Img", f"{PLAYER_NAME}.jpg")).convert_alpha()

    def show_profile(self, main_menu_surface):
        profile_img = transform.scale(self.__profile, self.__pos.size_tuple)
        main_menu_surface.blit(profile_img, self.__pos.img_coord)


class ProfilePos:
    __SIZE_RATIO = 18

    def __init__(self, pos):
        self.__pos = pos

    @property
    def img_coord(self):
        return self.__x, self.__y

    @property
    def __x(self):
        return self.__pos.record_x + 6

    @property
    def __y(self):
        return self.__pos.record_y + 5

    @property
    def size_tuple(self):
        return self.__size, self.__size

    @property
    def __size(self):
        return self.__pos.height // self.__SIZE_RATIO


class RecordPos:
    def __init__(self, display):
        self.__display = display
        self.__record_y = 0

    @property
    def record_width(self):
        return 550

    @property
    def record_height(self):
        return 60

    @property
    def height(self):
        return self.__display.height

    @property
    def record_y(self):
        return self.__record_y

    def set_record_y(self, padding):
        self.__record_y = 200 + padding

    @property
    def record_x(self):
        return 1000
