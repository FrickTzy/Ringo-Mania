from pygame import Rect, draw
from Frontend.Settings import IMPORT_MAP, Color
from Frontend.Mania_Window.Stats.Combo.combo import ComboCounter
from Frontend.Mania_Window.Rectangle.lane_manager import LaneManager, ImportCircles
from Frontend.Mania_Window.Stats.Show_Acc.show_acc import ShowAcc
from Backend.timer import IntervalTimer


class Rectangle:
    __RECT_COLOR = Color.PURPLE

    def __init__(self, *, show_acc, maps, display, combo_counter: ComboCounter,
                 mini_timer: IntervalTimer, map_status):
        self.__pos = RectanglePos(display=display)
        self.show_acc: ShowAcc = show_acc
        self.map_status = map_status
        self.combo_counter = combo_counter
        self.map_manager = maps
        self.imported = IMPORT_MAP
        self.rect = Rect(self.__pos.rectangle_x, 0, self.__pos.rectangle_width, self.__pos.rectangle_height)
        self.lane_manager: LaneManager = LaneManager(window=self.__pos.window, display=display,
                                                     timer=mini_timer, rectangle_pos=self.__pos)
        self.import_circle_manager = ImportCircles(self.lane_manager)

    def run(self, current_time: int, pause: bool):
        if not pause and not self.map_status.failed_or_finished:
            self.lane_manager.init_fall_circles(map_manager=self.map_manager, current_time=current_time)
            self.check_circles_if_out()
        self.show(pause=pause)

    def check_circles_if_out(self):
        if circles_out := self.lane_manager.check_circles_if_out():
            self.combo_counter.miss_score(amount_of_circles=circles_out)
            self.show_acc.update_acc(0)

    def show(self, pause):
        draw.rect(self.__pos.window, self.__RECT_COLOR, self.rect)
        self.lane_manager.show_all_circles(height=self.__pos.rectangle_height, pause=pause)
        self.show_acc.show_acc(window=self.__pos.window, window_size=self.__pos.get_window_size)

    def update_rect(self):
        self.rect = Rect(self.__pos.rectangle_x, 0, self.__pos.rectangle_width, self.__pos.rectangle_height)
        self.__update_circles()

    def restart(self):
        self.lane_manager.clear_all_circles()
        if self.imported:
            self.import_circle_manager.reset()

    def __update_circles(self):
        if self.map_status.failed_or_finished:
            return
        self.lane_manager.update_circles()

    def key_pressed(self, index: int):
        self.lane_manager.check_slider_key_input(lane=index)
        if hit_info := self.lane_manager.check_key_input_range(key_lane_input=index):
            if self.map_status.failed:
                return
            grade, stats = hit_info
            acc, score = stats
            self.combo_counter.hit_circle_successfully(grade=grade, acc=acc, score=acc)
            self.show_acc.update_acc(score=score)

    @property
    def rectangle_width(self):
        return self.__pos.rectangle_width

    @property
    def pos_class(self):
        return self.__pos


class RectanglePos:
    __RECTANGLE_WIDTH_CAP = 650
    __RECTANGLE_WIDTH_RATIO = 2.4

    def __init__(self, display):
        self.__display = display

    @property
    def rectangle_width(self):
        rectangle_width = self.__display.width // self.__RECTANGLE_WIDTH_RATIO
        if rectangle_width >= self.__RECTANGLE_WIDTH_CAP:
            rectangle_width = self.__RECTANGLE_WIDTH_CAP
        return rectangle_width

    @property
    def rectangle_x(self):
        return self.__display.width / 2 - (self.rectangle_width / 2)

    @property
    def rectangle_height(self):
        return self.__display.height

    @property
    def window(self):
        return self.__display.window

    @property
    def get_window_size(self):
        return self.__display.get_window_size
