from pygame import Rect, draw
from Stuff.Ringo_Mania.Frontend.settings import RECT_COLOR, \
    IMPORT_MAP
from Stuff.Ringo_Mania.Frontend.combo import ComboCounter
from Stuff.Ringo_Mania.Frontend.lane_manager import LaneManager, ImportCircles
from Stuff.Ringo_Mania.Frontend.show_acc import ShowAcc
from Stuff.Ringo_Mania.Backend.timer import MiniTimer


class Rectangle:
    def __init__(self, *, show_acc, window, music, maps, display, combo_counter: ComboCounter, pause,
                 mini_timer: MiniTimer, map_status):
        self.display = display
        self.show_acc: ShowAcc = show_acc
        self.map_status = map_status
        self.music = music
        self.window = window
        self.combo_counter = combo_counter
        self.map_manager = maps
        self.imported = IMPORT_MAP
        self.pause = pause
        self.rect = Rect(self.display.rectangle_x, 0, self.display.rectangle_width, self.display.height)
        self.lane_manager: LaneManager = LaneManager(window=self.window, display=self.display, timer=mini_timer)
        self.import_circle_manager = ImportCircles(self.lane_manager)

    def run(self, current_time: int):
        self.lane_manager.init_fall_circles(map_manager=self.map_manager, current_time=current_time)
        self.lane_manager.check_circles_if_out()
        self.show()

    def show(self):
        draw.rect(self.window, RECT_COLOR, self.rect)
        self.lane_manager.show_all_circles(height=self.display.height, pause=self.pause.is_paused)
        self.show_acc.show_acc(window=self.window, window_size=self.display.get_window_size)

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
        self.lane_manager.check_key_input_range(key_lane_input=index)
        self.music.play_hit_sound()
