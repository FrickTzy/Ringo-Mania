from pygame import Rect, draw, image, transform
from Frontend.settings import GRAY_PURPLE
from Frontend.Helper_Files.button_event_handler import ButtonEventHandler
from Backend.Map_Info.Map_Infos.map_info import MapInfo
from Backend.Map_Info import MapImage
from .map_bar_text import MapBarText


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
        self.__profile = MapBarBackgroundPreview(pos=self.__pos, image_status=self.__map_bar_info.song_name_status)
        self.__state = state
        self.__text = MapBarText(map_info=self.__map_bar_info, pos=self.__pos)

    def show(self, main_menu_surface, y: int):
        self.__update_rect(y=y)
        self.__draw_rect(main_menu_surface=main_menu_surface)
        self.__profile.show_profile(main_menu_surface=main_menu_surface, chosen=self.__chosen)
        self.__text.show_text(main_menu_surface=main_menu_surface)
        self.__viewed = True

    def check_if_clicked(self):
        self.__button_handler.check_buttons_for_clicks(starting_pos=self.__pos.record_starting_coord,
                                                       size=self.__pos.record_size,
                                                       command=lambda: self.set_chosen())

    def set_chosen(self):
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

    @property
    def song_name(self):
        return self.__map_bar_info.song_file_name


class MapBarInfo:
    def __init__(self, song_name, play_rank, star_rating=3.0):
        self.__map_info = MapInfo(song_name=song_name)
        self.__play_rank = play_rank
        self.__star_rating = star_rating

    @property
    def song_name(self):
        return self.__map_info.song_name

    @property
    def song_file_name(self):
        return self.__map_info.song_file_name

    @property
    def song_artist(self):
        return self.__map_info.song_artist

    @property
    def song_name_status(self):
        return self.__map_info.map_background_status


class MapBarBackgroundPreview:
    __OPACITY = 100

    def __init__(self, pos, image_status):
        name, is_an_anime = image_status
        self.__pos = BackgroundPreviewPos(pos=pos)
        self.__image_checker = MapImage()
        self.__background_image = image.load(
            self.__image_checker.get_image(title=name, anime_song=is_an_anime)).convert_alpha()
        self.__final_img = None

    def show_profile(self, main_menu_surface, chosen: bool = False):
        self.__image_setup(chosen=chosen)
        main_menu_surface.blit(self.__final_img, self.__pos.img_coord)

    def __image_setup(self, chosen: bool = False):
        if self.__final_img is not None:
            return
        self.__final_img = transform.scale(self.__background_image, self.__pos.size_tuple)
        if not chosen:
            self.__final_img.set_alpha(self.__OPACITY)

    def show_static_profile(self, main_menu_surface, y: int):
        profile_img = transform.scale(self.__background_image, self.__pos.size_tuple)
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
        return self.__pos.record_x + 558

    def y(self, y=0):
        if not y:
            return self.__pos.record_y + 6
        return y + 5

    @property
    def size_tuple(self):
        return 135, 94


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
        return 107

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
