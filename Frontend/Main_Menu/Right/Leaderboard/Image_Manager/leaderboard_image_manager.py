from pygame import transform


class LeaderboardImageManager:
    __original_sized_record_profiles: dict
    __current_sized_record_profiles: dict

    def __init__(self, profile_image_manager, display):
        self.__profile_image_manager = profile_image_manager
        self.__init_record_images()
        self.__size_manager = SizeManager(display=display)

    def __init_record_images(self):
        self.__original_sized_record_profiles = self.__profile_image_manager.copy_player_images()
        self.__current_sized_record_profiles = self.__profile_image_manager.copy_player_images()

    def get_profile_image(self, player_name):
        if player_name not in self.__current_sized_record_profiles:
            return self.__current_sized_record_profiles[self.__profile_image_manager.default_file_name]
        return self.__current_sized_record_profiles[player_name]

    def __set_size(self, profile_size: tuple):
        for name, image in self.__original_sized_record_profiles.items():
            self.__current_sized_record_profiles[name] = transform.scale(image, profile_size)

    def check_if_resize(self):
        if self.__size_manager.check_if_resize():
            self.__set_size(profile_size=self.__size_manager.profile_size)


class SizeManager:
    __SIZE_RATIO = 18
    __current_height = 0

    def __init__(self, display):
        self.__display = display

    def check_if_resize(self):
        if (height := self.__display.get_window_size[1]) != self.__current_height:
            self.__current_height = height
            return True
        return False

    @property
    def profile_size(self):
        return self.__size, self.__size

    @property
    def __size(self):
        return self.__current_height // self.__SIZE_RATIO
