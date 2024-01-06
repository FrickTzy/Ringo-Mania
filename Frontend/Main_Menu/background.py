from pygame import image, transform
from Backend.Map_Info import MapImage


class Background:
    __OPACITY = 255

    def __init__(self):
        self.__image_checker = MapImage()
        self.__image = None
        self.__background = None

    def show_background(self, map_background_status: tuple, window, window_size: tuple):
        name, is_an_anime = map_background_status
        if self.__image is None:
            self.__image = image.load(self.__image_checker.get_image(title=name, anime_song=is_an_anime))
        self.__background = transform.scale(self.__image, window_size)
        self.__background.set_alpha(self.__OPACITY)
        window.blit(self.__background, (0, 0))

    @property
    def background(self):
        return self.__background

    @property
    def image(self):
        return self.__image
