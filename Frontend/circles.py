import pygame
import os
from Stuff.Ringo_Mania.Frontend.settings import BOTTOM_CIRCLE, CIRCLE_SIZE


class Circle:
    def __init__(self, window, lane, lane_coord, size=CIRCLE_SIZE, img="Purp.png"):
        self.__circle_img = pygame.transform.scale(pygame.image.load(os.path.join("Frontend\Img", img)).convert_alpha(),
                                                   (size, size))
        self.window = window
        self.lane_coord = lane_coord
        self.lane = lane
        self.__img = img

    def draw_circles(self, y: int = BOTTOM_CIRCLE) -> None:
        self.window.blit(self.__circle_img, (self.lane_coord[self.lane], y))

    def change_lane_coord(self, coord: dict) -> None:
        self.lane_coord = coord

    def change_size(self, size) -> None:
        self.__circle_img = pygame.transform.scale(
            pygame.image.load(os.path.join("Frontend\Img", self.__img)).convert_alpha(),
            (size, size))

    @property
    def circle_img(self):
        return self.__circle_img
