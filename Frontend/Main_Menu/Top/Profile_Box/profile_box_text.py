from pygame import font
from Frontend.Settings import Color


class ProfileBoxText:
    __COLOR = Color.WHITE

    def __init__(self, player_info: dict, display, profile_box_pos):
        self.__player_info = player_info
        self.__font = Font()
        self.__pos = TextPos(display=display, profile_box_pos=profile_box_pos)

    def show_text(self, surface, profile_image_end_x):
        self.__font.check_if_update_font(height=self.__pos.height)
        self.__show_player_name(surface=surface, profile_image_end_x=profile_image_end_x)
        self.__show_player_rin_points(surface=surface, profile_image_end_x=profile_image_end_x)
        self.__show_player_accuracy(surface=surface, profile_image_end_x=profile_image_end_x)
        self.__show_player_level(surface=surface, profile_image_end_x=profile_image_end_x)

    def __show_player_name(self, surface, profile_image_end_x):
        player_name_text = self.__font.player_name_font.render(self.__player_info["player_name"], True, self.__COLOR)
        surface.blit(player_name_text, self.__pos.player_name_pos(image_end_x=profile_image_end_x))

    def __show_player_rin_points(self, surface, profile_image_end_x):
        rin_points_string = f"Performance: {self.__player_info['rin_points']}"
        rin_points_text = self.__font.player_info_font.render(rin_points_string, True, self.__COLOR)
        surface.blit(rin_points_text, self.__pos.player_info_pos(image_end_x=profile_image_end_x, nth_position=1))

    def __show_player_accuracy(self, surface, profile_image_end_x):
        accuracy_string = f"Accuracy: {self.__player_info['accuracy']}"
        accuracy_text = self.__font.player_info_font.render(accuracy_string, True, self.__COLOR)
        surface.blit(accuracy_text, self.__pos.player_info_pos(image_end_x=profile_image_end_x, nth_position=2))

    def __show_player_level(self, surface, profile_image_end_x):
        level_string = f"Lvl {self.__player_info['level']}"
        level_text = self.__font.player_info_font.render(level_string, True, self.__COLOR)
        surface.blit(level_text, self.__pos.player_info_pos(image_end_x=profile_image_end_x, nth_position=3))


class Font:
    __PLAYER_NAME_FONT_RATIO = 45
    __PLAYER_INFO_FONT_RATIO = 69
    __current_height = 0

    def __init__(self):
        self.__player_name_font = font.SysFont("arialblack", 20)
        self.__player_info_font = font.SysFont("arialblack", 10)

    @property
    def player_name_font(self):
        return self.__player_name_font

    @property
    def player_info_font(self):
        return self.__player_info_font

    def __update_font(self, height) -> None:
        self.__player_name_font = font.SysFont("arialblack", self.__player_font_size(height=height))
        self.__player_info_font = font.SysFont("arialblack", self.__player_info_size(height=height))

    def check_if_update_font(self, height):
        if self.__current_height == height:
            return
        self.__update_font(height=height)
        self.__current_height = height

    def __player_font_size(self, height):
        return int(height // self.__PLAYER_NAME_FONT_RATIO)

    def __player_info_size(self, height):
        return int(height // self.__PLAYER_INFO_FONT_RATIO)

    def player_name_text_size(self, text: str) -> tuple[int, int]:
        width, height = self.__player_name_font.size(text)
        return width, height


class TextPos:
    __X_RATIO = 4
    __PLAYER_NAME_RATIO, __PLAYER_INFO_RATIO = 39, 11.43

    def __init__(self, display, profile_box_pos):
        self.__display = display
        self.__profile_box_pos = profile_box_pos

    @property
    def __x(self):
        return self.__display.width // self.__X_RATIO

    def player_name_pos(self, image_end_x):
        return self.__text_x(image_end_x=image_end_x), self.__player_name_y

    @property
    def __player_name_y(self):
        return self.__profile_box_pos.starting_y + 14

    def player_info_pos(self, image_end_x, nth_position):
        return self.__text_x(image_end_x=image_end_x), self.__player_name_y + 11 + \
               self.__player_info_y_interval * nth_position

    @property
    def __player_info_y_interval(self):
        return 16

    @staticmethod
    def __text_x(image_end_x):
        return image_end_x + 15

    @property
    def height(self):
        return self.__display.height
