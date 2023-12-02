from pygame import Rect, draw
from Stuff.Ringo_Mania.Frontend.settings import RECT_COLOR, \
    IMPORT_MAP
from Stuff.Ringo_Mania.Frontend.combo import ComboCounter
from Stuff.Ringo_Mania.Frontend.lane_manager import LaneManager, ImportCircles
from Stuff.Ringo_Mania.Frontend.show_acc import ShowAcc
from Stuff.Ringo_Mania.Backend.timer import MiniTimer


class Rectangle:
    def __init__(self, *, show_acc, maps, display, combo_counter: ComboCounter,
                 mini_timer: MiniTimer, map_status):
        self.display = display
        self.show_acc: ShowAcc = show_acc
        self.map_status = map_status
        self.combo_counter = combo_counter
        self.map_manager = maps
        self.imported = IMPORT_MAP
        self.rect = Rect(self.display.rectangle_x, 0, self.display.rectangle_width, self.display.height)
        self.lane_manager: LaneManager = LaneManager(window=self.display.window, display=self.display, timer=mini_timer)
        self.import_circle_manager = ImportCircles(self.lane_manager)

    def run(self, current_time: int, pause: bool):
        if not pause and not self.map_status.failed_or_finished:
            self.lane_manager.init_sliders()
            self.check_circles_if_out()
        self.show(pause=pause)

    def check_circles_if_out(self):
        if circles_out := self.lane_manager.check_circles_if_out():
            self.combo_counter.miss_score(amount_of_circles=circles_out)
            self.show_acc.update_acc(0)

    def show(self, pause):
        draw.rect(self.display.window, RECT_COLOR, self.rect)
        self.lane_manager.show_all_circles(height=self.display.height, pause=pause)
        self.show_acc.show_acc(window=self.display.window, window_size=self.display.get_window_size)

    def update_rect(self):
        self.rect = Rect(self.display.rectangle_x, 0, self.display.rectangle_width, self.display.height)
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
        if hit_info := self.lane_manager.check_key_input_range(key_lane_input=index):
            if self.map_status.failed:
                return
            grade, stats = hit_info
            acc, score = stats
            self.combo_counter.hit_circle_successfully(grade=grade, acc=acc, score=acc)
            self.show_acc.update_acc(score=score)
