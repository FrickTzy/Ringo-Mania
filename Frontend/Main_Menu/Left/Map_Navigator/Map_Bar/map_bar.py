from pygame import Rect, draw, image, transform
from Frontend.Settings import Color
from Frontend.Helper_Files.button_event_handler import ButtonEventHandler
from Backend.Map_Info.Map_Infos.map_info import MapInfo
from Backend.Map_Info import MapImage
from Backend.timer import DelayTimer
from .map_bar_text import MapBarText


class MapBar:
    __COLOR = Color.GRAY_PURPLE
    __CHOSEN_COLOR = Color.DARK_PURPLE
    __OPACITY = 190
    __CLICK_INTERVAL = 80
    __viewed = False

    def __init__(self, song_name: str, play_rank: str, display, pos, state, index_manager, index):
        self.__index = index
        self.__pos = RecordPos(display=display, pos=pos, index=self.__index)
        self.__map_bar_info = MapBarInfo(song_name=song_name, play_rank=play_rank)
        self.__rect = Rect(self.__pos.record_x, self.__pos.record_y, self.__pos.record_width,
                           self.__pos.record_height)
        self.__button_handler = ButtonEventHandler()
        self.__profile = MapBarBackgroundPreview(pos=self.__pos, image_status=self.__map_bar_info.song_name_status)
        self.__state = state
        self.__text = MapBarText(map_info=self.__map_bar_info, pos=self.__pos)
        self.__index_manager = index_manager
        self.__timer = DelayTimer()

    def show(self, main_menu_surface, y: int):
        self.__update_rect(y=y)
        if self.is_chosen:
            self.__show_chosen(main_menu_surface=main_menu_surface)
        else:
            self.__show_not_chosen(main_menu_surface=main_menu_surface)
        self.__check_if_out_of_bounds()

    def __show_chosen(self, main_menu_surface):
        self.__draw_rect(main_menu_surface=main_menu_surface, is_chosen=True)
        self.__profile.show_profile(main_menu_surface=main_menu_surface, is_chosen=True)
        self.__text.show_text(main_menu_surface=main_menu_surface, is_chosen=True)

    def __show_not_chosen(self, main_menu_surface):
        self.__draw_rect(main_menu_surface=main_menu_surface, is_chosen=False)
        self.__profile.show_profile(main_menu_surface=main_menu_surface, is_chosen=False)
        self.__text.show_text(main_menu_surface=main_menu_surface, is_chosen=False)

    def check_if_clicked(self):
        if self.is_chosen:
            self.__timer.check_delay_ms(self.__CLICK_INTERVAL)
            if self.__timer.timer_finished:
                self.__button_handler.check_buttons_for_clicks(starting_pos=self.__pos.record_starting_coord,
                                                               size=self.__pos.record_size,
                                                               command=lambda: self.__state.show_play_window())
        else:
            self.__button_handler.check_buttons_for_clicks(starting_pos=self.__pos.record_starting_coord,
                                                           size=self.__pos.record_size,
                                                           command=lambda: self.set_chosen())
            self.__timer.reset_timer()

    def key_hit(self):
        self.__state.show_play_window()

    def set_chosen(self):
        self.__index_manager.set_index(index=self.__index)

    @property
    def is_chosen(self):
        return self.__index == self.__index_manager.current_index

    @property
    def is_viewed(self) -> bool:
        return self.__viewed

    def __check_if_out_of_bounds(self):
        if self.__pos.record_y >= 800 or self.__pos.record_y <= 25:
            self.__viewed = False
        else:
            self.__viewed = True

    def __draw_rect(self, main_menu_surface, is_chosen: bool = False):
        if is_chosen:
            r, g, b = self.__CHOSEN_COLOR
            self.__rect.width = self.__pos.chosen_record_width
            draw.rect(main_menu_surface, (r, g, b, self.__OPACITY), self.__rect)
        else:
            r, g, b = self.__COLOR
            draw.rect(main_menu_surface, (r, g, b, self.__OPACITY), self.__rect)

    def __update_rect(self, y: int):
        self.__pos.set_record_y()
        self.__rect = Rect(self.__pos.record_x, self.__pos.record_y, self.__pos.record_width,
                           self.__pos.record_height)

    @property
    def song_name(self):
        return self.__map_bar_info.song_file_name

    @property
    def song_file_name(self):
        return self.__map_bar_info.song_file_name

    @property
    def image(self):
        return self.__profile.image

    @property
    def change_top_index(self):
        return self.__pos.record_y > 80


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

    def show_profile(self, main_menu_surface, is_chosen: bool):
        self.__image_setup(chosen=is_chosen)
        img_coord = self.__pos.chosen_img_coord if is_chosen else self.__pos.img_coord
        main_menu_surface.blit(self.__final_img, img_coord)

    def __image_setup(self, chosen: bool = False):
        self.__final_img = transform.scale(self.__background_image, self.__pos.size_tuple)
        self.__set_opacity(chosen=chosen)

    def __set_opacity(self, chosen: bool):
        if chosen:
            self.__final_img.set_alpha(255)
        else:
            self.__final_img.set_alpha(self.__OPACITY)

    @property
    def image(self):
        return self.__background_image


class BackgroundPreviewPos:
    __SIZE_RATIO = 18
    __X_RATIO = 1.27
    __WIDTH_RATIO, __HEIGHT_RATIO = 5, 1.14

    def __init__(self, pos):
        self.__pos = pos

    @property
    def img_coord(self):
        return self.__x, self.y

    @property
    def chosen_img_coord(self):
        return self.__chosen_x, self.y

    @property
    def __x(self):
        return self.__pos.record_x + self.__pos.record_width // self.__X_RATIO

    @property
    def __chosen_x(self):
        return self.__pos.record_x + 633

    @property
    def y(self):
        return self.__pos.record_y + 6

    @property
    def size_tuple(self):
        return self.__width, self.__height

    @property
    def __width(self):
        return self.__pos.record_width // self.__WIDTH_RATIO

    @property
    def __height(self):
        return self.__pos.record_height // self.__HEIGHT_RATIO


class RecordPos:
    def __init__(self, display, pos, index):
        self.__display = display
        self.__pos = pos
        self.__record_y = 0
        self.__index = index

    @property
    def record_width(self):
        return 700

    @property
    def record_height(self):
        return 107

    @property
    def chosen_record_width(self):
        return 780

    @property
    def record_size(self):
        return self.record_width, self.record_height

    @property
    def height(self):
        return self.__display.height

    def set_record_y(self):
        self.__record_y = self.__pos.record_starting_y + self.__pos.starting_record_pos(index=self.__index)

    @property
    def record_y(self):
        return self.__record_y

    @property
    def record_x(self):
        return self.__pos.leaderboard_x

    @property
    def record_starting_coord(self):
        return self.record_x, self.record_y
