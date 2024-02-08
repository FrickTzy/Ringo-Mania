from pygame import Rect, draw
from Frontend.Settings import Color
from .map_bar_preview import MapBarBackgroundPreview
from .map_bar_text import MapBarText
from .map_bar_event_handler import MapBarEventHandler
from .map_bar_info import MapBarInfo
from .map_bar_pos import MapBarPos
from .Map_Bar_Animation import MapBarAnimation


class MapBar:
    __COLOR = Color.GRAY_PURPLE
    __CHOSEN_COLOR = Color.DARK_PURPLE
    __OPACITY = 190
    __viewed = False

    def __init__(self, song_name: str, play_rank: str, display, pos, state, index_manager, index):
        self.__index = index
        self.__pos = MapBarPos(display=display, pos=pos, index=self.__index)
        self.__map_bar_info = MapBarInfo(song_name=song_name, play_rank=play_rank)
        self.__rect = Rect(self.__pos.record_x, self.__pos.record_y, self.__pos.record_width,
                           self.__pos.record_height)
        self.__profile = MapBarBackgroundPreview(pos=self.__pos, image_status=self.__map_bar_info.song_name_status)
        self.__state = state
        self.__text = MapBarText(map_info=self.__map_bar_info, pos=self.__pos)
        self.__index_manager = index_manager
        self.__map_bar_animation = MapBarAnimation(is_chosen=self.is_chosen, map_bar_pos=self.__pos)
        self.__event_handler = MapBarEventHandler(index=self.__index, index_manager=index_manager, pos=self.__pos,
                                                  state=state)

    def show(self, main_menu_surface):
        self.update_rect()
        self.__map_bar_animation.check_for_animation(is_chosen=self.is_chosen,
                                                     is_hovered=self.check_if_hovered())
        if self.is_chosen:
            self.__show_chosen(main_menu_surface=main_menu_surface)
        else:
            self.__show_not_chosen(main_menu_surface=main_menu_surface)
        self.__check_if_out_of_bounds()

    def show_filtered(self, main_menu_surface, index: int):
        self.__update_filtered_rect(index=index)
        self.__map_bar_animation.check_for_animation(is_chosen=self.is_chosen,
                                                     is_hovered=self.check_if_hovered())
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
        return self.__event_handler.check_if_clicked(chosen=self.is_chosen)

    def key_hit(self):
        self.__state.show_play_window()

    def set_chosen(self):
        self.__event_handler.set_chosen()

    @property
    def is_chosen(self):
        return self.__index == self.__index_manager.current_index

    @property
    def is_viewed(self) -> bool:
        return self.__viewed

    def __check_if_out_of_bounds(self):
        if self.__pos.record_y >= 800 or self.__pos.record_y <= 10:
            self.__viewed = False
        else:
            self.__viewed = True

    def __draw_rect(self, main_menu_surface, is_chosen: bool = False):
        self.__rect.width = self.__pos.current_map_bar_width
        r, g, b = self.__CHOSEN_COLOR if is_chosen else self.__COLOR
        draw.rect(main_menu_surface, (r, g, b, self.__OPACITY), self.__rect)

    def update_rect(self):
        self.__pos.set_record_y()
        self.__rect = Rect(self.__pos.record_x, self.__pos.record_y, self.__pos.record_width,
                           self.__pos.record_height)

    def __update_filtered_rect(self, index):
        self.__pos.set_record_y_filter(index=index)
        self.__rect = Rect(self.__pos.record_x, self.__pos.record_y, self.__pos.record_width,
                           self.__pos.record_height)

    @property
    def song_name(self):
        return self.__map_bar_info.song_name

    @property
    def song_file_name(self):
        return self.__map_bar_info.song_file_name

    @property
    def song_artist(self):
        return self.__map_bar_info.song_artist

    @property
    def image(self):
        return self.__profile.image

    @property
    def change_top_index(self):
        """This is what to change when top bar not showing"""
        return self.__pos.record_y > 30

    @property
    def position(self):
        return self.__pos.record_x, self.__pos.record_y

    def check_if_hovered(self):
        return self.__event_handler.check_if_hovered()

    def reset_pos(self):
        self.__pos.reset_y()
