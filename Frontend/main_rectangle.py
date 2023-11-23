import pygame
from pygame import Rect, draw, key
from random import randrange, getrandbits
from Stuff.Ringo_Mania.Frontend.settings import RECT_COLOR, MAX_CIRCLES_PER_FRAME, KEY_BINDS, \
    KEY_DELAY, HIT_SOUNDS, NUM_OF_LANES, MAX_LIFE, MULTI_CIRCLE_CHANCE, \
    MULTIPLE_CIRCLE_FREQ, ACC_CATEGORIES_POINTS, IMPORT_MAP, OKAY_lIFE_DMG
from Stuff.Ringo_Mania.Frontend.circles import Circle
from Stuff.Ringo_Mania.Frontend.falling_circles import FallingCircle
from Stuff.Ringo_Mania.Frontend.combo import ComboCounter
from Stuff.Ringo_Mania.Frontend.show_acc import ShowAcc
from Stuff.Ringo_Mania.Frontend.pause import Pause


class Rectangle:
    def __init__(self, *, window, music, maps, timer, display, combo_counter: ComboCounter):
        self.display = display
        self.show_acc = ShowAcc()
        self.rect = Rect(self.display.rectangle_x, 0, self.display.rectangle_width, self.display.height)
        self.timer = timer
        self.music = music
        self.failed = False
        self.map_finished = False
        self.main_window = window
        self.current_circle = 0
        self.falling_circles = []
        self.circles = []
        self.lanes_taken = []
        self.imported_lanes = []
        self.imported_lanes_index = 0
        self.map = []
        self.last = pygame.time.get_ticks()
        self.tap_time = pygame.time.get_ticks()
        self.combo_counter = combo_counter
        self.tapped = False
        self.map_manager = maps
        self.imported = IMPORT_MAP
        self.finished_importing = False
        self.pause = Pause(circles=self.falling_circles, music=self.music)

    def run(self):
        self.fall_circles_init()
        if not self.pause.is_paused:
            self.remove_fall_circles()
        self.show()
        self.detect_key()

    def update_rect(self):
        if self.display.check_window_size():
            self.rect = Rect(self.display.rectangle_x, 0, self.display.rectangle_width, self.display.height)
            self.update_circles()
            self.update_bar()
            self.update_fall_circles()

    def update_bar(self):
        self.combo_counter.change_life_bar_coord(self.display.life_bar_coord_x)

    def update_fall_circles(self):
        if self.failed or self.map_finished:
            return
        for circle in self.falling_circles:
            circle.change_size(self.display.circle_size)
            circle.update_hit_box(self.display.circle_size)
            circle.change_lane_coord(self.display.circle_position)

    def update_circles(self):
        self.circles.clear()
        self.init_circles()

    def show(self):
        self.update_rect()
        draw.rect(self.main_window, RECT_COLOR, self.rect)
        for index, circle in enumerate(self.circles):
            circle.draw_circles(y=self.display.bottom_circle_y)
        if self.check_pause():
            return
        for fall_circle in self.falling_circles:
            fall_circle.draw_circle(self.display.height, speed=self.display.falling_speed)
        self.show_acc.show_acc(self.main_window, x=self.display.acc_identifier_x, y=self.display.acc_identifier_y)

    def check_pause(self) -> bool:
        if self.pause.is_paused:
            self.pause.show_pause()
            return True
        return False

    def init_circles(self):
        for i in range(4):
            self.circles.append(
                Circle(self.main_window, i, self.display.circle_position, size=self.display.circle_size))

    def fall_circles_init(self):
        if self.imported:
            self.import_circles_init()
        if self.map_finished or self.failed:
            self.music.fade_music()
            if not self.failed and not self.imported:
                self.map_manager.overwrite_map()
            return
        if len(self.falling_circles) >= MAX_CIRCLES_PER_FRAME:
            return
        self.fall_circles()

    def fall_circles(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last >= self.display.interval:
            self.last = current_time
            if self.pause.is_paused:
                return
            if self.imported:
                if self.imported_lanes_index >= len(self.imported_lanes) - 1:
                    self.map_finished = True
                    return
                for circle_index in self.imported_lanes[self.imported_lanes_index]:
                    self.falling_circles.append(FallingCircle(self.main_window, circle_index))
                self.imported_lanes_index += 1
            else:
                self.lanes_taken = []
                self.falling_circles.append(
                    FallingCircle(self.main_window, self.lane_setter(), lane_coord=self.display.circle_position,
                                  circle_size=self.display.circle_size))
                self.multiple_circles_process()
                self.map_manager.convert_to_map_list(self.lanes_taken, self.timer.current_time)

    def import_circles_init(self):
        if self.finished_importing:
            return
        for circle_list in self.map_manager.import_map():
            circle_on_column = []
            for lane_index, lane in enumerate(circle_list.split(",")):
                if "O" in lane:
                    circle_on_column.append(lane_index)
            self.imported_lanes.append(circle_on_column)
        self.finished_importing = True

    def multiple_circles_process(self, current_circle=2):
        if current_circle > NUM_OF_LANES:
            return
        if self.double_circle_chance(MULTIPLE_CIRCLE_FREQ[str(current_circle)]):
            self.falling_circles.append(
                FallingCircle(self.main_window, self.lane_setter(), lane_coord=self.display.circle_position,
                              circle_size=self.display.circle_size))
            self.multiple_circles_process(current_circle + 1)

    def lane_setter(self):
        lane = randrange(0, NUM_OF_LANES)
        while lane in self.lanes_taken:
            lane = randrange(0, NUM_OF_LANES)
        self.lanes_taken.append(lane)
        return lane

    @staticmethod
    def double_circle_chance(chance=MULTI_CIRCLE_CHANCE):
        for _ in range(chance):
            outcome = getrandbits(1)
            if not outcome:
                return False
        return True

    def remove_fall_circles(self, key_lane="null"):
        if self.failed:
            return
        for fall_circle in self.falling_circles:
            if fall_circle.out:
                self.falling_circles.remove(fall_circle)
                if self.combo_counter.combo != 0:
                    self.music.play_miss_sound()
                self.combo_counter.combo = 0
                self.combo_counter.add_clicked_circles(0)
                self.combo_counter.lose_life()
                self.combo_counter.miss()
                self.show_acc.update_acc(0)
            if key_lane != "null":
                if key_lane == fall_circle.lane:
                    if self.display.last_hit_window >= fall_circle.hit_box.y > self.display.first_hit_window:
                        self.falling_circles.remove(fall_circle)
                        grade, stats = self.determine_acc(fall_circle.hit_box.y)
                        acc, score = stats
                        self.combo_counter.combo += 1
                        self.combo_counter.compute_score(score)
                        self.show_acc.update_acc(score)
                        self.combo_counter.add_clicked_circles(acc)
                        if grade == "Okay":
                            self.combo_counter.lose_life(OKAY_lIFE_DMG)
                            continue
                        if self.combo_counter.life < MAX_LIFE:
                            self.combo_counter.compute_life()

    def detect_key(self):
        current_time = pygame.time.get_ticks()
        key_pressed = key.get_pressed()
        for keys in KEY_BINDS:
            self.pause.check_pause(key_pressed)
            if key_pressed[eval(keys)]:
                self.remove_fall_circles(KEY_BINDS[keys])
                if not HIT_SOUNDS:
                    return
                if current_time - self.tap_time >= KEY_DELAY:
                    self.tap_time = current_time
                    self.music.play_hit_sound()

    def determine_acc(self, y_position):
        score_category = ""
        hit_windows: dict = self.display.acc_category_hit_window
        category_list = list(hit_windows.keys())
        for category, acc_range in hit_windows.items():
            if (index := category_list.index(category)) == 0:
                continue
            if y_position > acc_range[1]:
                score_category = category_list[index - 1]
                break
            elif y_position < acc_range[0]:
                score_category = category_list[index - 1]
                break
            elif category == "Amazing":
                if acc_range[0] <= y_position <= acc_range[1]:
                    score_category = category
                    break

        return score_category, ACC_CATEGORIES_POINTS[score_category]
