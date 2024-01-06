from pygame import Rect, draw, image, transform
from os import path
from Frontend.settings import GRAY_PURPLE, PLAYER_NAME
from Frontend.Helper_Files.button_event_handler import ButtonEventHandler
from Backend.Map_Info.Map_Infos.map_info import MapInfo


class MapBar:
    __COLOR = GRAY_PURPLE
    __OPACITY = 190
    __viewed = False
    __chosen = False

    def __init__(self, song_name: str, play_rank: str, display, pos, state):
        self.__pos = RecordPos(display=display, pos=pos)
        self.__map_bar_info = MapBarInfo(song_name=song_name, play_rank=play_rank)
        self.__rect = Rect(self.__pos.record_x, self.__pos.record_y, self.__pos.record_width,
                           self.__pos.record_height)
        self.__button_handler = ButtonEventHandler()
        self.__profile = MapBarBackgroundPreview(pos=self.__pos)
        self.__state = state

    def show(self, main_menu_surface, image, y: int):
        self.__update_rect(y=y)
        self.__draw_rect(main_menu_surface=main_menu_surface)
        self.__profile.show_profile(main_menu_surface=main_menu_surface, image=image)
        self.__viewed = True

    def check_if_clicked(self):
        self.__button_handler.check_buttons_for_clicks(starting_pos=self.__pos.record_starting_coord,
                                                       size=self.__pos.record_size,
                                                       command=lambda: self.__set_chosen())

    def __set_chosen(self):
        self.__chosen = True

    @property
    def is_chosen(self):
        return self.__chosen

    @property
    def is_viewed(self) -> bool:
        return self.__viewed

    def __check_if_out_of_bounds(self):
        if self.__pos.record_y >= 690 or self.__pos.record_y <= 165:
            return True

    def __draw_rect(self, main_menu_surface):
        r, g, b = self.__COLOR
        draw.rect(main_menu_surface, (r, g, b, self.__OPACITY), self.__rect)

    def __update_rect(self, y: int):
        self.__pos.set_record_y(padding=y)
        self.__rect = Rect(self.__pos.record_x, self.__pos.record_y, self.__pos.record_width,
                           self.__pos.record_height)


class MapBarInfo:
    def __init__(self, song_name, play_rank, star_rating=3.0):
        self.__map_info = MapInfo(song_name=song_name)
        self.__play_rank = play_rank
        self.__star_rating = star_rating


class MapBarBackgroundPreview:
    def __init__(self, pos):
        self.__pos = BackgroundPreviewPos(pos=pos)
        self.__profile = image.load(path.join("Frontend\Main_Menu\Img", f"{PLAYER_NAME}.jpg")).convert_alpha()

    def show_profile(self, main_menu_surface, image):
        profile_img = transform.scale(image, self.__pos.size_tuple)
        main_menu_surface.blit(profile_img, self.__pos.img_coord)

    def show_static_profile(self, main_menu_surface, y: int):
        profile_img = transform.scale(self.__profile, self.__pos.size_tuple)
        main_menu_surface.blit(profile_img, (self.__pos.img_coord[0], self.__pos.y(y=y)))


class BackgroundPreviewPos:
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
        return 125, 98


class RecordPos:
    def __init__(self, display, pos):
        self.__display = display
        self.__pos = pos
        self.__record_y = 0

    @property
    def record_width(self):
        return 700

    @property
    def record_height(self):
        return 108

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
