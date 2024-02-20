from pygame import Rect, draw
from .text_stat import TextStats
from Frontend.Settings import Color
from Frontend.Helper_Files.button_event_handler import ButtonEventHandler


class Record:
    __COLOR = Color.DARK_PURPLE
    __OPACITY = 200
    __viewed = False

    def __init__(self, play_dict, display, pos, state, leaderboard_image_manager):
        self.__pos = RecordPos(display=display, pos=pos)
        self.__play_dict = play_dict
        self.__text_stats = TextStats(play_info=play_dict, pos=self.__pos)
        self.__rect = Rect(self.__pos.record_x, self.__pos.record_y, self.__pos.record_width,
                           self.__pos.record_height)
        self.__button_handler = ButtonEventHandler()
        self.__profile = RecordProfile(pos=self.__pos,
                                       leaderboard_image_manager=leaderboard_image_manager,
                                       player_name=play_dict["player_name"])
        self.__state = state

    def show(self, main_menu_surface, y: int):
        self.__update_rect(y=y)
        if self.__check_if_out_of_bounds():
            self.__viewed = False
            return
        self.__draw_rect(main_menu_surface=main_menu_surface)
        self.__profile.show_profile(main_menu_surface=main_menu_surface)
        self.__text_stats.show_text(main_menu_surface=main_menu_surface)
        self.__viewed = True

    def check_if_clicked(self):
        clicked = self.__button_handler.check_buttons_for_clicks(starting_pos=self.__pos.record_starting_coord,
                                                                 size=self.__pos.record_size,
                                                                 command=lambda: self.__state.show_score_screen(
                                                                     current_play=self.__play_dict))
        if clicked:
            return True
        else:
            return False

    @property
    def is_viewed(self) -> bool:
        return self.__viewed

    def __check_if_out_of_bounds(self):
        if self.__pos.record_y >= 690 or self.__pos.record_y <= 165:
            return True

    def show_static(self, main_menu_surface, y: int):
        self.__rect.y = y
        self.__draw_rect(main_menu_surface=main_menu_surface)
        self.__profile.show_static_profile(main_menu_surface=main_menu_surface, y=y)
        self.__text_stats.show_static_text(main_menu_surface=main_menu_surface, y=y)

    def check_if_clicked_best_play(self, y: int):
        return self.__button_handler.check_buttons_for_clicks(starting_pos=(self.__pos.record_x, y),
                                                              size=self.__pos.record_size,
                                                              command=lambda: self.__state.show_score_screen(
                                                                  current_play=self.__play_dict))

    def __draw_rect(self, main_menu_surface):
        r, g, b = self.__COLOR
        draw.rect(main_menu_surface, (r, g, b, self.__OPACITY), self.__rect)

    def __update_rect(self, y: int):
        self.__pos.set_record_y(padding=y)
        self.__rect.x = self.__pos.record_x
        self.__rect.y = self.__pos.record_y
        self.__rect.width = self.__pos.record_width
        self.__rect.height = self.__pos.record_height


class RecordProfile:
    def __init__(self, pos, leaderboard_image_manager, player_name):
        self.__pos = ProfilePos(pos=pos)
        self.__leaderboard_image_manager = leaderboard_image_manager
        self.__player_name = player_name

    def show_profile(self, main_menu_surface):
        main_menu_surface.blit(self.__leaderboard_image_manager.get_profile_image(player_name=self.__player_name),
                               self.__pos.img_coord)

    def show_static_profile(self, main_menu_surface, y: int):
        main_menu_surface.blit(self.__leaderboard_image_manager.get_profile_image(player_name=self.__player_name),
                               (self.__pos.img_coord[0], self.__pos.y(y=y)))


class ProfilePos:
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
