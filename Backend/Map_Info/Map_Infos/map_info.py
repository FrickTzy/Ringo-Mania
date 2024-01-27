from pygame import transform
from copy import copy
from Backend.Map_Info.Map_Infos.map_info_checker import MapInfoChecker


class MapInfo:
    changed = True

    def __init__(self, song_name: str = None, song_artist: str = "IDK", map_maker: str = "Dudesalp"):
        self.__song_file_name = song_name
        self.__artist = song_artist
        self.__map_maker = map_maker
        self.__info_checker = MapInfoChecker()
        self.__image_manager = ImageManager()

    @property
    def song_file_name(self):
        return self.__song_file_name

    @property
    def song_name(self):
        return self.__check_for_anime_titles()

    @property
    def __anime_title(self):
        if "Op" in self.__song_file_name:
            index = self.__song_file_name.index("Op")
        else:
            index = self.__song_file_name.index("Ed")
        return self.__song_file_name[:index - 1]

    @property
    def map_background_status(self):
        if "-" not in self.__song_file_name:
            return self.song_artist, False
        else:
            return self.__anime_title, True

    def __check_for_anime_titles(self):
        if "-" not in self.__song_file_name:
            return self.__song_file_name
        index = self.__song_file_name.index("-")
        return self.__song_file_name[index + 2::]

    @property
    def song_artist(self):
        return self.__info_checker.get_song_artist(song_name=self.__song_file_name)

    @property
    def map_maker(self):
        return self.__map_maker

    @property
    def song_info(self):
        return f"{self.song_name} - {self.song_artist}"

    def set_song_name(self, song_name):
        self.__song_file_name = song_name
        self.changed = True

    @property
    def current_background_image(self):
        return self.__image_manager.current_background_image

    @property
    def low_opacity_background_image(self):
        return self.__image_manager.low_opacity_background_image

    def set_background(self, image, window_size):
        self.__image_manager.set_background(image=image, window_size=window_size)


class ImageManager:
    __current_background_image = None
    __low_opacity_background_image = None

    @property
    def low_opacity_background_image(self):
        return self.__low_opacity_background_image

    @property
    def current_background_image(self):
        return self.__current_background_image

    def set_background(self, image, window_size):
        self.__current_background_image = transform.scale(image, window_size)
        self.__low_opacity_background_image = copy(self.__current_background_image)
        self.__low_opacity_background_image.set_alpha(15)
