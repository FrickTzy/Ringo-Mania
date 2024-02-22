from pygame import transform, Surface
from copy import copy


class ProfileImage:
    def __init__(self, image_manager, player_name, profile_box_pos, display):
        self.__image = self.__copy_profile_image(image_manager=image_manager, player_name=player_name)
        self.__size_manager = SizeManager(display=display)
        self.__pos = PosManager(profile_box_pos=profile_box_pos)

    @staticmethod
    def __copy_profile_image(image_manager, player_name):
        return copy(image_manager.get_profile_image(player_name=player_name))

    def show(self, surface: Surface):
        self.__check_if_resize()
        surface.blit(self.__image, self.__pos.profile_image_pos)

    def __check_if_resize(self):
        if self.__size_manager.check_if_resize():
            self.__image = transform.scale(self.__image, self.__size_manager.profile_image_size)

    @property
    def end_x(self):
        return self.__pos.x + self.__size_manager.profile_image_size[0]


class SizeManager:
    __current_height = 0

    def __init__(self, display):
        self.__display = display

    def check_if_resize(self):
        if self.__current_height != (height := self.__display.get_window_size[1]):
            self.__current_height = height
            return True
        return False

    @property
    def profile_image_size(self):
        return self.__profile_size, self.__profile_size

    @property
    def __profile_size(self):
        return 75


class PosManager:
    def __init__(self, profile_box_pos):
        self.__profile_box_pos = profile_box_pos

    @property
    def profile_image_pos(self):
        return self.x, 18

    @property
    def x(self):
        return self.__profile_box_pos.starting_x + 10
