from pygame import image, transform
from Backend.Map_Info import MapImage


class Background:
    __OPACITY = 15
    __current_name: str
    __is_an_anime: bool

    def __init__(self):
        self.__image_checker = MapImage()
        self.__image = None

    def show_background(self, map_background_status: tuple, screen, window_size: tuple):
        self.__check_if_change_background(map_background_status=map_background_status)
        background = transform.scale(self.__image, window_size)
        background.set_alpha(self.__OPACITY)
        screen.blit(background, (0, 0))

    def __check_if_change_background(self, map_background_status: tuple):
        name, is_an_anime = map_background_status
        if self.__image is None:
            self.__current_name, self.__is_an_anime = name, is_an_anime
            self.__image = image.load(
                self.__image_checker.get_image(title=self.__current_name, anime_song=self.__is_an_anime))
        if name != self.__current_name or is_an_anime != self.__is_an_anime:
            self.__current_name, self.__is_an_anime = name, is_an_anime
            self.__image = image.load(self.__image_checker.get_image(title=name, anime_song=is_an_anime))
