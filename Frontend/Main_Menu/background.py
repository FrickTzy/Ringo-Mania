from pygame import transform
from Backend.Map_Info import MapImage


class Background:
    __OPACITY = 255

    def __init__(self):
        self.__image_checker = MapImage()
        self.__background = None

    def show_background(self, image, window, window_size: tuple):
        self.__background = transform.scale(image, window_size)
        self.__background.set_alpha(self.__OPACITY)
        window.blit(self.__background, (0, 0))

    @property
    def background(self):
        return self.__background
