from Stuff.Ringo_Mania.Frontend.Mania_Window.Rectangle.lane import Lane
from Stuff.Ringo_Mania.Frontend.Mania_Window.Misc.display import Display
from random import randrange, getrandbits
from Stuff.Ringo_Mania.Backend.timer import IntervalTimer


class LaneManager:
    __NUM_OF_LANES = 4
    __MULTIPLE_CIRCLE_CHANCE = {
        "Slider": 2,
        "2": 2,
        "3": 6,
        "4": 8,
    }

    def __init__(self, window, display: Display, timer: IntervalTimer):
        self.lane_circle_manager = LaneCircleManager(display=display)
        self.lanes_taken = []
        lane_coord = self.lane_circle_manager.circle_position
        self.lanes: [Lane] = [Lane(lane_coord[0]), Lane(lane_coord[1]), Lane(lane_coord[2]), Lane(lane_coord[3])]
        self.window = window
        self.mini_timer: IntervalTimer = timer
        self.set_up_timer_interval()

    def set_up_timer_interval(self):
        self.mini_timer.change_interval(interval=self.lane_circle_manager.interval)

    def init_fall_circles(self, map_manager, current_time: int):
        if self.mini_timer.time_interval_finished():
            self.reset_lanes_taken()
            if self.slider_chance():
                self.init_sliders()
            self.add_a_circle_to_a_lane(self.lane_setter())
            self.multiple_circles_process()
            map_manager.convert_to_map_list(self.lanes_taken, current_time)

    def init_sliders(self):
        if self.mini_timer.time_interval_finished():
            self.reset_lanes_taken()
            self.check_for_sliders()
            self.check_if_end_sliders()
            if len(self.lanes_taken) == self.__NUM_OF_LANES:
                return
            self.add_a_slider_to_a_lane(self.lane_setter())

    def check_if_end_sliders(self):
        for lane in self.lanes:
            lane.check_if_end_slider()

    def check_for_sliders(self):
        for index, lane in enumerate(self.lanes):
            if lane.check_if_lane_taken():
                self.lanes_taken.append(index)

    def add_a_circle_to_a_lane(self, lane):
        self.lanes[lane].add_fall_circle(window=self.window, size=self.lane_circle_manager.circle_size)

    def add_a_slider_to_a_lane(self, lane):
        if lane is not None:
            self.lanes[lane].add_sliders(window=self.window, size=self.lane_circle_manager.circle_size,
                                         min_len=self.lane_circle_manager.interval)

    def multiple_circles_process(self, current_circle=2):
        if current_circle > self.__NUM_OF_LANES:
            return
        if self.double_circle_chance(self.__MULTIPLE_CIRCLE_CHANCE[str(current_circle)]):
            self.add_a_circle_to_a_lane(self.lane_setter())
            self.multiple_circles_process(current_circle + 1)

    def show_all_circles(self, height, pause):
        self.show_sliders_to_all_lanes(height=height, pause=pause)
        self.show_hitting_circles_to_all_lanes()
        self.show_fall_circles_to_all_lanes(height=height, pause=pause)

    def show_fall_circles_to_all_lanes(self, height, pause: bool):
        for lane in self.lanes:
            lane.show_fall_circles(height=height, speed=self.lane_circle_manager.circle_speed, pause=pause)

    def show_hitting_circles_to_all_lanes(self):
        for lane in self.lanes:
            lane.show_hitting_circle(window=self.window, hitting_circle_y=self.lane_circle_manager.bottom_circle_y,
                                     size=self.lane_circle_manager.circle_size)

    def show_sliders_to_all_lanes(self, height, pause: bool):
        for lane in self.lanes:
            lane.show_sliders(height=height, speed=self.lane_circle_manager.circle_speed, pause=pause)

    def clear_all_circles(self):
        for lane in self.lanes:
            lane.clear_circles()

    def update_circles(self):
        for lane in self.lanes:
            lane.update_circles(self.lane_circle_manager.circle_size)

    @staticmethod
    def double_circle_chance(chance):
        for _ in range(chance):
            outcome = getrandbits(1)
            if not outcome:
                return False
        return True

    def slider_chance(self):
        return self.double_circle_chance(self.__MULTIPLE_CIRCLE_CHANCE["Slider"])

    def reset_lanes_taken(self) -> None:
        self.lanes_taken = []

    def lane_setter(self):
        if len(self.lanes_taken) == self.__NUM_OF_LANES:
            return
        lane = randrange(0, self.__NUM_OF_LANES)
        while lane in self.lanes_taken:
            lane = randrange(0, self.__NUM_OF_LANES)
        self.lanes_taken.append(lane)
        return lane

    def check_circles_if_out(self):
        circle_quantity = 0
        for index, lane in enumerate(self.lanes):
            if lane.check_circles_if_out():
                circle_quantity += 1
        return circle_quantity

    def check_key_input_range(self, key_lane_input):
        if (circle_y := self.lanes[key_lane_input].check_circles_if_hit(
                first_hit_window=self.lane_circle_manager.first_hit_window,
                last_hit_window=self.lane_circle_manager.last_hit_window)):
            return self.lane_circle_manager.determine_acc(circle_y)
        return False

    def check_slider_key_input(self, lane):
        if circle_y := self.lanes[lane].check_sliders_if_hit(first_hit_window=self.lane_circle_manager.first_hit_window,
                                                             last_hit_window=self.lane_circle_manager.last_hit_window,
                                                             speed=self.lane_circle_manager.circle_speed):
            return self.lane_circle_manager.determine_acc(circle_y)


class LaneCircleManager:
    __CIRCLE_SIZE_TO_RECT_WIDTH = 3.92
    __BOTTOM_CIRCLE_RATIO = 1.20
    __HIT_WINDOW_PADDING = (60, 85)

    def __init__(self, display: Display):
        self.display = display
        self.circle_hit_window = CircleHitWindow()

    @property
    def circle_position(self):
        circle_start_padding = 6 + self.display.rectangle_width // 100
        circle_x_start = self.display.rectangle_x + circle_start_padding
        between_circle_padding = self.display.rectangle_width // 4.25
        return {
            0: circle_x_start,
            1: circle_x_start + between_circle_padding * 1,
            2: circle_x_start + between_circle_padding * 2,
            3: circle_x_start + between_circle_padding * 3}

    @property
    def circle_size(self):
        return int(self.display.rectangle_width / self.__CIRCLE_SIZE_TO_RECT_WIDTH)

    @property
    def bottom_circle_y(self):
        return self.display.height // self.__BOTTOM_CIRCLE_RATIO - self.display.width // 20

    @property
    def circle_speed(self):
        # FALLING_SPEED + self.circle_size // SPEED_RATIO
        return 24

    @property
    def interval(self):
        # self.falling_speed * INTERVAL_RATIO
        return 180

    @property
    def first_hit_window(self):
        return self.bottom_circle_y - self.__HIT_WINDOW_PADDING[0]

    @property
    def last_hit_window(self):
        return self.bottom_circle_y + self.__HIT_WINDOW_PADDING[1]

    def determine_acc(self, y_position):
        score_category: str = ""
        hit_windows: dict = self.circle_hit_window.acc_category_hit_window(self.bottom_circle_y)
        category_list: list = list(hit_windows.keys())
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

        return score_category, self.circle_hit_window.acc_category_points[score_category]


class CircleHitWindow:
    __AMAZING_SCORE_PADDING = (10, 30)
    __PERFECT_SCORE_PADDING = 35
    __GOOD_SCORE_PADDING = (15, 10)
    __OKAY_SCORE_PADDING = 10
    __ACC_CATEGORIES_POINTS = {
        "Okay": (50, 50),
        "Good": (75, 100),
        "Perfect": (100, 300),
        "Amazing": (100, 320)
    }

    def __init__(self):
        self.bottom_circle_y = 0

    @property
    def acc_category_points(self):
        return self.__ACC_CATEGORIES_POINTS

    @property
    def amazing_hit_window(self):
        return self.bottom_circle_y + self.__AMAZING_SCORE_PADDING[0], self.bottom_circle_y + \
               self.__AMAZING_SCORE_PADDING[1]

    @property
    def perfect_hit_window(self):
        return self.amazing_hit_window[0] - self.__PERFECT_SCORE_PADDING, self.amazing_hit_window[
            1] + self.__PERFECT_SCORE_PADDING

    @property
    def good_hit_window(self):
        return self.perfect_hit_window[0] - self.__GOOD_SCORE_PADDING[0], self.perfect_hit_window[1] + \
               self.__GOOD_SCORE_PADDING[1]

    @property
    def okay_hit_window(self):
        return self.good_hit_window[0] - self.__OKAY_SCORE_PADDING, self.good_hit_window[1] + self.__OKAY_SCORE_PADDING

    def acc_category_hit_window(self, bottom_circle_y):
        self.bottom_circle_y = bottom_circle_y
        return {
            "Okay": self.okay_hit_window,
            "Good": self.good_hit_window,
            "Perfect": self.perfect_hit_window,
            "Amazing": self.amazing_hit_window
        }


class ImportCircles:
    def __init__(self, lane_manager):
        self.imported_lanes_index = 0
        self.imported_lanes = []
        self.__finished_importing = False
        self.lane_manager: LaneManager = lane_manager

    @property
    def finished_importing(self) -> bool:
        return self.__finished_importing

    def import_fall_circles(self):
        if self.imported_lanes_index >= len(self.imported_lanes) - 1:
            self.__finished_importing = True
            return
        for circle_lane in self.imported_lanes[self.imported_lanes_index]:
            self.lane_manager.add_a_circle_to_a_lane(lane=circle_lane)
        self.imported_lanes_index += 1

    def reset(self):
        self.__finished_importing = False
        self.import_fall_circles()
        self.imported_lanes_index = 0
