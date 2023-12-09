from Frontend.Mania_Window.Rectangle.Circles.circles import Circle
from pygame import Rect
from Frontend.settings import CIRCLE_SIZE, FALLING_SPEED, HEIGHT


class FallingCircle(Circle):
    def __init__(self, window, lane_x, circle_size=CIRCLE_SIZE, img="Purp.png"):
        super().__init__(circle_size, img)
        self.y = -100
        self.hit_box = Rect(lane_x, self.y, circle_size, circle_size)
        self.window = window
        self.out = False

    def draw_circles(self, height=HEIGHT, speed=FALLING_SPEED, pause=False):
        self.window.blit(super().circle_img, (self.hit_box.x, self.hit_box.y))
        if not pause:
            self.hit_box.y += speed
            self.__check_out_of_screen(height=height)

    def update_hit_box(self, lane_x, size) -> None:
        self.hit_box = Rect(lane_x, self.y, size, size)

    def __check_out_of_screen(self, height):
        if self.hit_box.y >= height:
            self.out = True
            del self
