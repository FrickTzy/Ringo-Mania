from Stuff.Ringo_Mania.Frontend.circles import Circle
from pygame import Rect
from Stuff.Ringo_Mania.Frontend.settings import CIRCLE_SIZE, FALLING_SPEED, LANES, HEIGHT


class FallingCircle(Circle):
    def __init__(self, window, lane, lane_coord=LANES, circle_size=CIRCLE_SIZE, img="Purp.png"):
        super().__init__(window, lane, lane_coord, circle_size, img)
        self.y = -100
        self.hit_box = Rect(self.lane_coord[self.lane], self.y, CIRCLE_SIZE, CIRCLE_SIZE)
        self.out = False

    def draw_circle(self, height=HEIGHT, speed=FALLING_SPEED, pause=False):
        self.window.blit(super().circle_img, (self.hit_box.x, self.hit_box.y))
        if not pause:
            self.hit_box.y += speed
            self.out_of_screen(height)

    def update_hit_box(self, size) -> None:
        self.hit_box = Rect(self.lane_coord[self.lane], self.y, size, size)

    def out_of_screen(self, height=HEIGHT):
        if self.hit_box.y >= height:
            self.out = True
            del self
