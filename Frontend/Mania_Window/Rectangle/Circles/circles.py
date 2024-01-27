from pygame import transform
from Frontend.Settings import DEFAULT_CIRCLE_SIZE


class Circle:
    def __init__(self, circle_image_manager, circle_size=DEFAULT_CIRCLE_SIZE):
        self.__circle_image_manager = circle_image_manager
        self.__circle_img = transform.scale(self.__circle_image_manager.circle_image, (circle_size, circle_size))

    def draw_circles(self, window, x: int, y: int) -> None:
        window.blit(self.__circle_img, (x, y))

    def change_size(self, size) -> None:
        self.__circle_img = transform.scale(self.__circle_image_manager.circle_image, (size, size))

    @property
    def circle_img(self):
        return self.__circle_img
