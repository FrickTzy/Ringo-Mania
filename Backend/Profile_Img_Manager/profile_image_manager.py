from glob import glob
from pygame import image
from copy import copy


class ProfileImageManager:
    __PATH = "Backend/Profile_Img_Manager/Player_Images"
    __POSSIBLE_IMG_EXTENSIONS = [".jpg", ".jpeg", ".png"]
    __DEFAULT_FILE = "__Guest__"
    __player_images = {}

    def __init__(self):
        self.__init_profile_images()

    def __init_profile_images(self):
        for profile_file in self.__get_all_files():
            self.__player_images[self.__remove_file_name_suffixes(file_name=profile_file)] = \
                image.load(self.__get_path(file=profile_file))

    def copy_player_images(self):
        return copy(self.__player_images)

    def get_profile_image(self, player_name):
        if not self.__check_if_player_profile_exist(player_name=player_name):
            return self.__player_images[self.__DEFAULT_FILE]
        return self.__player_images[player_name]

    def __check_if_player_profile_exist(self, player_name):
        if player_name in self.__player_images:
            return True
        return False

    def __get_all_files(self):
        return glob("*.*", root_dir=self.__PATH)

    def __get_path(self, file):
        return f"{self.__PATH}/{file}"

    def __remove_file_name_suffixes(self, file_name: str):
        for img_extension in self.__POSSIBLE_IMG_EXTENSIONS:
            if not file_name.endswith(img_extension):
                continue
            return file_name.removesuffix(img_extension)

    @property
    def default_file_name(self):
        return self.__DEFAULT_FILE


if __name__ == "__main__":
    pass
