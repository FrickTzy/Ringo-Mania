from pygame import Rect, draw, image, transform
from os import path
from .text_stat import TextStats
from Frontend.settings import DARK_PURPLE, PLAYER_NAME
from Frontend.Helper_Files.button_event_handler import ButtonEventHandler


class Record:
    __COLOR = DARK_PURPLE
    __OPACITY = 210

    def __init__(self, play_dict, display, pos, state):
        self.__pos = RecordPos(display=display, pos=pos)
        self.__play_dict = play_dict
        self.__text_stats = TextStats(play_info=play_dict, pos=self.__pos)
        self.__rect = Rect(self.__pos.record_x, self.__pos.record_y, self.__pos.record_width,
                           self.__pos.record_height)
        self.__button_handler = ButtonEventHandler()
        self.__profile = RecordProfile(pos=self.__pos)
        self.__state = state

    def show(self, main_menu_surface, y: int):
        self.__update_rect(y=y)
        if self.__check_if_out_of_bounds():
            return
        self.__draw_rect(main_menu_surface=main_menu_surface)
        self.__profile.show_profile(main_menu_surface=main_menu_surface)
        self.__text_stats.show_text(main_menu_surface=main_menu_surface)
        self.__button_handler.check_buttons_for_clicks(starting_pos=self.__pos.record_starting_coord,
                                                       size=self.__pos.record_size,
                                                       command=lambda: self.__state.show_score_screen(
                                                           current_play=self.__play_dict))

    def __check_if_out_of_bounds(self):
        if self.__pos.record_y >= 690 or self.__pos.record_y <= 165:
            return True

    def show_static(self, main_menu_surface, y: int):
        self.__rect.y = y
        self.__draw_rect(main_menu_surface=main_menu_surface)
        self.__profile.show_static_profile(main_menu_surface=main_menu_surface, y=y)
        self.__text_stats.show_static_text(main_menu_surface=main_menu_surface, y=y)
        self.__button_handler.check_buttons_for_clicks(starting_pos=(self.__pos.record_x, y),
                                                       size=self.__pos.record_size,
                                                       command=lambda: self.__state.show_score_screen(
                                                           current_play=self.__play_dict))

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

    def show_static_profile(self, main_menu_surface, y: int):
        profile_img = transform.scale(self.__profile, self.__pos.size_tuple)
        main_menu_surface.blit(profile_img, (self.__pos.img_coord[0], self.__pos.y(y=y)))


class ProfilePos:
    __SIZE_RATIO = 18

    def __init__(self, pos):
        self.__pos = pos

    @property
    def img_coord(self):
        return self.__x, self.y()

    @property
    def __x(self):
        return self.__pos.record_x + 6

    def y(self, y=0):
        if not y:
            return self.__pos.record_y + 5
        return y + 5

    @property
    def size_tuple(self):
        return self.__size, self.__size

    @property
    def __size(self):
        return self.__pos.height // self.__SIZE_RATIO


class RecordPos:
    def __init__(self, display, pos):
        self.__display = display
        self.__pos = pos
        self.__record_y = 0

    @property
    def record_width(self):
        return self.__pos.leaderboard_width

    @property
    def record_height(self):
        return 60

    @property
    def record_size(self):
        return self.record_width, self.record_height

    @property
    def height(self):
        return self.__display.height

    def set_record_y(self, padding):
        self.__record_y = self.__pos.record_starting_y + padding

    @property
    def record_y(self):
        return self.__record_y

    @property
    def record_x(self):
        return self.__pos.leaderboard_x

    @property
    def record_starting_coord(self):
        return self.record_x, self.record_y
