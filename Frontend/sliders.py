from Stuff.Ringo_Mania.Frontend.circles import Circle
from Stuff.Ringo_Mania.Frontend.settings import CIRCLE_SIZE, FALLING_SPEED, DARK_PURPLE, BLACK
from Stuff.Ringo_Mania.Backend.timer import MiniTimer
from pygame import Rect, draw
from random import randrange


class Sliders(Circle):
    __LEN_PER_BODY = 100
    __SLIDER_COLOR = BLACK
    __SLIDER_END_PERCENTAGE = 50
    __MIN_SLIDER_LEN = 180

    """
    A slider consists of three parts: the starting circle, the main body, and the ending circle.
    """

    def __init__(self, window, lane_x, min_slider_len, circle_size=CIRCLE_SIZE, img="Purp.png"):
        super().__init__(circle_size, img)
        self.y = -100
        self.slider_head_hit_box = Rect(lane_x, self.y, circle_size, CIRCLE_SIZE)
        self.slider_body_hit_box = Rect(lane_x + circle_size // 5.39, self.y, circle_size - circle_size // 2.92,
                                        self.__LEN_PER_BODY)
        self.slider_tail_hit_box = Rect(lane_x, self.y - circle_size / 2, circle_size, CIRCLE_SIZE)
        self.window = window
        self.out = False
        self.slider_ended = False
        self.min_slider_len_finished = False
        self.minimum_slider_len_checker = MiniTimer(interval=min_slider_len)
        self.hit_head = False
        self.hit_tail = False
        self.total_len = self.__LEN_PER_BODY

    def draw_slider(self, height, speed, pause):
        self.check_if_min_len_finished()
        self.__show_slider_body(speed=speed, pause=pause)
        if not self.slider_ended:
            self.__add_slider_body(speed=speed, pause=pause)
        else:
            self.__check_out_of_screen(height=height)
        if self.hit_head:
            return
        self.__start_slider(pause=pause, speed=speed)

    def __add_slider_body(self, pause, speed=FALLING_SPEED):
        if pause:
            return
        self.slider_body_hit_box.height += speed

    def check_if_min_len_finished(self):
        if self.minimum_slider_len_checker.time_interval_finished():
            self.min_slider_len_finished = True

    def __show_slider_body(self, speed, pause):
        draw.rect(self.window, self.__SLIDER_COLOR, self.slider_body_hit_box)
        if self.slider_ended and not self.hit_tail:
            self.window.blit(self.circle_img, (self.slider_tail_hit_box.x, self.slider_tail_hit_box.y))
            if not pause:
                self.slider_tail_hit_box.y += speed
                self.slider_body_hit_box.y += speed
                self.total_len += speed

    def get_slider_y(self):
        return self.slider_body_hit_box.y + self.total_len

    def remove_head(self):
        self.hit_head = True

    def remove_tail(self):
        self.hit_tail = True

    def __end_slider(self):
        self.slider_ended = True

    def check_if_end_slider(self):
        if randrange(1, 100 // self.__SLIDER_END_PERCENTAGE) == 1:
            self.__end_slider()

    def __start_slider(self, pause: bool, speed=FALLING_SPEED):
        self.window.blit(self.circle_img, (self.slider_head_hit_box.x, self.slider_head_hit_box.y))
        if not pause:
            self.slider_head_hit_box.y += speed

    def __check_out_of_screen(self, height):
        if self.slider_tail_hit_box.y >= height:
            self.out = True
            del self

    def hold_slider(self, speed):
        self.slider_body_hit_box.height -= speed
        self.total_len -= speed + 1
