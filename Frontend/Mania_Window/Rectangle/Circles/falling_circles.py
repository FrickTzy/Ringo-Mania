from Frontend.Mania_Window.Rectangle.Circles.circles import Circle
from pygame import Rect
from Frontend.Settings import FALLING_SPEED, HEIGHT, DEFAULT_CIRCLE_SIZE


class FallingCircle(Circle):
    __out = False

    def __init__(self, window, lane_x, circle_image_manager, circle_size=DEFAULT_CIRCLE_SIZE):
        super().__init__(circle_image_manager=circle_image_manager, circle_size=circle_size)
        self.__y = -100
        self.__hit_box = Rect(lane_x, self.__y, circle_size, circle_size)
        self.__window = window

    def draw_circles(self, height=HEIGHT, speed=FALLING_SPEED, pause=False):
        self.__window.blit(super().circle_img, (self.__hit_box.x, self.__hit_box.y))
        if not pause:
            self.__hit_box.y += speed
            self.__check_out_of_screen(height=height)

    def update_hit_box(self, lane_x, size) -> None:
        self.__hit_box = Rect(lane_x, self.__y, size, size)

    def check_if_hit(self, first_hit_window, last_hit_window):
        if last_hit_window >= self.__hit_box.y > first_hit_window:
            return self.__hit_box.y
        return False

    def __check_out_of_screen(self, height):
        if self.__hit_box.y >= height:
            self.__out = True
            del self

    @property
    def hit_box(self):
        return self.__hit_box

    @property
    def out(self):
        return self.__out
