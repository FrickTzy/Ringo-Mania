from pygame import image, transform
from os import path
from Frontend.Settings import PLAYER_NAME


class RecordProfileImage:
    def __init__(self):
        self.__profile = image.load(path.join("Frontend\Main_Menu\Img", f"{PLAYER_NAME}.jpg")).convert_alpha()

    def set_size(self, profile_size_tuple: tuple):
        self.__profile = transform.scale(self.__profile, profile_size_tuple)

    @property
    def profile_image(self):
        return self.__profile
