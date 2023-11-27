from Stuff.Ringo_Mania.Frontend.circles import Circle
from pygame import Rect
from Stuff.Ringo_Mania.Frontend.settings import CIRCLE_SIZE, FALLING_SPEED, LANES, HEIGHT


class FallingCircle(Circle):
    def __init__(self, window, lane_x, circle_size=CIRCLE_SIZE, img="Purp.png"):
        super().__init__(circle_size, img)
        self.y = -100
        self.hit_box = Rect(lane_x, self.y, CIRCLE_SIZE, CIRCLE_SIZE)
        self.window = window
        self.out = False

    def draw_circles(self, height=HEIGHT, speed=FALLING_SPEED, pause=False):
        self.window.blit(super().circle_img, (self.hit_box.x, self.hit_box.y))
        if not pause:
            self.hit_box.y += speed
            self.out_of_screen(height)

    def update_hit_box(self, lane_x, size) -> None:
        self.hit_box = Rect(lane_x, self.y, size, size)

    def out_of_screen(self, height=HEIGHT):
        if self.hit_box.y >= height:
            self.out = True
            del self
