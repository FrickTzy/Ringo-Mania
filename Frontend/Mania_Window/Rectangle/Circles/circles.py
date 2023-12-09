import pygame
import os
from Stuff.Ringo_Mania.Frontend.Mania_Window.settings import CIRCLE_SIZE


class Circle:
    def __init__(self, size=CIRCLE_SIZE, img="Purp.png"):
        self.__circle_img = pygame.transform.scale(
            pygame.image.load(os.path.join("Frontend\Mania_Window\Img", img)).convert_alpha(),
            (size, size))
        self.__img = img

    def draw_circles(self, window, x: int, y: int) -> None:
        window.blit(self.__circle_img, (x, y))

    def change_size(self, size) -> None:
        self.__circle_img = pygame.transform.scale(
            pygame.image.load(os.path.join("Frontend\Mania_Window\Img", self.__img)).convert_alpha(),
            (size, size))

    @property
    def circle_img(self):
        return self.__circle_img
