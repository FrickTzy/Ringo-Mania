from pygame import image, transform
from Backend.Map_Info import MapImage


class Background:
    __OPACITY = 15

    def __init__(self):
        self.__image_checker = MapImage()
        self.__image = None

    def show_background(self, map_background_status: tuple, screen, window_size: tuple):
        name, is_an_anime = map_background_status
        if self.__image is None:
            self.__image = image.load(self.__image_checker.get_image(title=name, anime_song=is_an_anime))
        background = transform.scale(self.__image, window_size)
        background.set_alpha(self.__OPACITY)
        screen.blit(background, (0, 0))
