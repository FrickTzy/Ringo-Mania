from Stuff.Ringo_Mania.Frontend.falling_circles import FallingCircle
from Stuff.Ringo_Mania.Frontend.settings import CIRCLE_HEIGHT, CIRCLE_WIDTH, FALLING_SPEED, LANES, HEIGHT
from pygame import Rect


class Sliders(FallingCircle):
    def __init__(self, window, lane):
        super().__init__(window, lane, "Purp.png")
        self.y = -100
        self.hit_box = Rect(LANES[self.lane], self.y, CIRCLE_WIDTH, CIRCLE_HEIGHT)
        self.out = False

    def draw_slider(self):
        self.window.blit(self.circle_img, (self.hit_box.x, self.hit_box.y))
        self.hit_box.y += FALLING_SPEED
        self.out_of_screen()
