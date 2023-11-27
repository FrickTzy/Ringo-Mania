from pygame import display, FULLSCREEN, mouse, RESIZABLE as PYRES, cursors
from Stuff.Ringo_Mania.Frontend.settings import WIDTH, HEIGHT, RESIZABLE, RECTANGLE_X, RECTANGLE_WIDTH, CIRCLE_X_START, \
    BETWEEN_CIRCLE_PADDING, CIRCLE_START_PADDING, CIRCLE_SIZE_TO_RECT_WIDTH, CIRCLE_SIZE, LIFE_BAR_PADDING, \
    RECTANGLE_WIDTH_CAP, LIFE_BAR_COORDINATES, FULL_SCREEN_VIEW, COMBO_Y_PADDING, \
    LIFE_BAR_Y_PADDING, LIFE_BAR_HEIGHT_RATIO, RECORD_Y_RATIO, NAME_Y_RATIO, ACC_IMG_SIZE, BOTTOM_CIRCLE_RATIO, \
    OKAY_SCORE_PADDING, AMAZING_SCORE_PADDING, PERFECT_SCORE_PADDING, GOOD_SCORE_PADDING, HIT_WINDOW_PADDING, \
    FALLING_SPEED, SPEED_RATIO, INTERVAL_RATIO, RECORD_Y_INTERVAL_RATIO, SCORE_PADDING_RATIO, ACC_Y_RATIO, \
    SCORE_X_RATIO, ACC_X_RATIO


class Display:
    def __init__(self):
        self.width, self.height = WIDTH, HEIGHT
        self.__rectangle_width = RECTANGLE_WIDTH
        self.__circle_x_start = CIRCLE_X_START
        self.__circle_size = CIRCLE_SIZE
        self.__rectangle_x = RECTANGLE_X
        self.__between_circle_padding = BETWEEN_CIRCLE_PADDING
        self.__circle_start_padding = CIRCLE_START_PADDING
        self.__life_bar_coordinates = LIFE_BAR_COORDINATES
        self.window = display.set_mode((self.width, self.height), PYRES if RESIZABLE else None)
        self.check_full_screen()
        self.set_title()

    def check_full_screen(self, full_screen=False):
        if FULL_SCREEN_VIEW or full_screen:
            self.width, self.height = 1600, 900
            self.window = display.set_mode((self.width, self.height), FULLSCREEN)
            mouse.set_visible(False)
            mouse.set_cursor(cursors.arrow)

    @property
    def get_window_size(self):
        return self.width, self.height

    @property
    def record_y_interval(self):
        return self.height // RECORD_Y_INTERVAL_RATIO

    @property
    def score_padding(self):
        return self.height // SCORE_PADDING_RATIO

    @property
    def falling_speed(self):
        # FALLING_SPEED + self.circle_size // SPEED_RATIO
        return 23

    @property
    def interval(self):
        # self.falling_speed * INTERVAL_RATIO
        return 180

    @property
    def acc_y(self):
        return self.height // ACC_Y_RATIO

    @property
    def rectangle_width(self):
        self.__rectangle_width = self.width / 2.2
        if self.__rectangle_width >= RECTANGLE_WIDTH_CAP:
            self.__rectangle_width = RECTANGLE_WIDTH_CAP
        return self.__rectangle_width

    @property
    def rectangle_x(self):
        self.__rectangle_x = self.width / 2 - (self.rectangle_width / 2)
        return self.__rectangle_x

    @property
    def score_pos_x(self):
        return self.width - (self.height // SCORE_X_RATIO)

    @property
    def acc_pos_x(self):
        return self.width - (self.height // ACC_X_RATIO)

    @property
    def acc_identifier_x(self):
        return self.width / 2 - (ACC_IMG_SIZE / 2)

    @property
    def acc_identifier_y(self):
        return self.height // 2.3

    @property
    def center(self) -> tuple[int, int]:
        return self.width // 2, self.height // 2

    def pause_text_pos(self, font_width):
        width, height = self.center
        return self.center_window_element(width, font_width), height / 1.6

    @staticmethod
    def center_window_element(width, element_width):
        return width - element_width / 2

    @property
    def combo_pos_y(self):
        return self.height - COMBO_Y_PADDING

    @property
    def circle_position(self):
        self.__circle_start_padding = 6 + self.__rectangle_width // 100
        self.__circle_x_start = self.__rectangle_x + self.__circle_start_padding
        self.__between_circle_padding = self.__rectangle_width // 4.25
        return {
            0: self.__circle_x_start,
            1: self.__circle_x_start + self.__between_circle_padding * 1,
            2: self.__circle_x_start + self.__between_circle_padding * 2,
            3: self.__circle_x_start + self.__between_circle_padding * 3,
        }

    @property
    def bottom_circle_y(self):
        return self.height // BOTTOM_CIRCLE_RATIO - self.width // 20

    @property
    def first_hit_window(self):
        return self.bottom_circle_y - HIT_WINDOW_PADDING[0]

    @property
    def last_hit_window(self):
        return self.bottom_circle_y + HIT_WINDOW_PADDING[1]

    @property
    def amazing_hit_window(self):
        return self.bottom_circle_y + AMAZING_SCORE_PADDING[0], self.bottom_circle_y + AMAZING_SCORE_PADDING[1]

    @property
    def perfect_hit_window(self):
        return self.amazing_hit_window[0] - PERFECT_SCORE_PADDING, self.amazing_hit_window[1] + PERFECT_SCORE_PADDING

    @property
    def good_hit_window(self):
        return self.perfect_hit_window[0] - GOOD_SCORE_PADDING[0], self.perfect_hit_window[1] + GOOD_SCORE_PADDING[1]

    @property
    def okay_hit_window(self):
        return self.good_hit_window[0] - OKAY_SCORE_PADDING, self.good_hit_window[1] + OKAY_SCORE_PADDING

    @property
    def acc_category_hit_window(self):
        return {
            "Okay": self.okay_hit_window,
            "Good": self.good_hit_window,
            "Perfect": self.perfect_hit_window,
            "Amazing": self.amazing_hit_window
        }

    @property
    def circle_size(self):
        self.__circle_size = int(self.__rectangle_width / CIRCLE_SIZE_TO_RECT_WIDTH)
        return self.__circle_size

    @property
    def life_bar_coord_x(self):
        return self.width / 2 + (self.__rectangle_width / 2) + LIFE_BAR_PADDING

    @property
    def life_bar_coord_y(self):
        return self.height - LIFE_BAR_Y_PADDING - self.__life_bar_height

    @property
    def __life_bar_height(self):
        return self.height // LIFE_BAR_HEIGHT_RATIO

    @property
    def record_y(self):
        return self.height // RECORD_Y_RATIO

    @property
    def name_y(self):
        return self.height // NAME_Y_RATIO

    @property
    def life_bar_coordinates(self):
        self.__life_bar_coordinates = (self.life_bar_coord_x, self.life_bar_coord_y, 10, self.__life_bar_height)
        return self.__life_bar_coordinates

    def check_window_size(self) -> bool:
        width, height = self.window.get_size()
        if width != self.width or height != self.height:
            self.height = height
            self.width = width
            return True
        else:
            return False

    @staticmethod
    def set_title():
        display.set_caption("Ringo Mania!")
