from pygame import Rect, draw, key
from Stuff.Ringo_Mania.Frontend.settings import RECT_COLOR, KEY_BINDS, \
    IMPORT_MAP
from Stuff.Ringo_Mania.Frontend.combo import ComboCounter
from Stuff.Ringo_Mania.Frontend.lane_manager import LaneManager, ImportCircles
from Stuff.Ringo_Mania.Frontend.show_acc import ShowAcc
from Stuff.Ringo_Mania.Backend.timer import MiniTimer


class Rectangle:
    def __init__(self, *, show_acc, window, music, maps, timer, display, combo_counter: ComboCounter, pause,
                 mini_timer, map_status):
        self.display = display
        self.show_acc: ShowAcc = show_acc
        self.map_status = map_status
        self.timer = timer
        self.music = music
        self.window = window
        self.mini_timer: MiniTimer = mini_timer
        self.combo_counter = combo_counter
        self.map_manager = maps
        self.imported = IMPORT_MAP
        self.pause = pause
        self.rect = Rect(self.display.rectangle_x, 0, self.display.rectangle_width, self.display.height)
        self.lane_manager: LaneManager = LaneManager(window=self.window, display=self.display)
        self.import_circle_manager = ImportCircles(self.lane_manager)

    def run(self):
        self.lane_manager.init_fall_circles(map_manager=self.map_manager, current_time=self.timer.current_time)
        self.lane_manager.check_circles_if_out()
        self.show()
        self.detect_key()

    def show(self):
        self.update_rect()
        draw.rect(self.window, RECT_COLOR, self.rect)
        self.lane_manager.show_all_circles(height=self.display.height, pause=self.pause.is_paused)
        self.show_acc.show_acc(window=self.window, window_size=self.display.get_window_size)

    def update_rect(self):
        if self.display.check_window_size():
            self.rect = Rect(self.display.rectangle_x, 0, self.display.rectangle_width, self.display.height)
            self.update_circles()
            self.update_bar()

    def restart(self):
        self.lane_manager.clear_all_circles()
        self.combo_counter.reset_all()
        self.show_acc.reset_acc()
        self.music.restart_music()
        self.timer.restart()
        self.map_status.failed = False
        if self.imported:
            self.import_circle_manager.reset()

    def update_bar(self):
        self.combo_counter.change_life_bar_coord(self.display.life_bar_coord_x)

    def update_circles(self):
        if self.map_status.failed_or_finished:
            return
        self.lane_manager.update_circles()

    def detect_key(self):
        key_pressed = key.get_pressed()
        if self.pause.check_pause(key_pressed):
            return
        for keys, index in KEY_BINDS.items():
            if key_pressed[eval(keys)]:
                self.lane_manager.check_key_input_range(index)
                self.music.play_hit_sound()
