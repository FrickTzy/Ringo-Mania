from pygame import image
from os import path


class CircleImage:
    __PATH = "Frontend\Mania_Window\Img"

    def __init__(self, img="Purp.png"):
        self.__circle_image = image.load(path.join(self.__PATH, img)).convert_alpha()

    @property
    def circle_image(self):
        return self.__circle_image
