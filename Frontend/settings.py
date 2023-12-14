from pygame import time

FULL_SCREEN_VIEW = True

HIT = "HIT"

WIDTH, HEIGHT = 1200, 700
RECTANGLE_WIDTH = WIDTH / 2.2  # 510
RECTANGLE_X = WIDTH / 2 - (RECTANGLE_WIDTH / 2)
CIRCLE_SIZE_TO_RECT_WIDTH = 3.92
CIRCLE_SIZE = int(RECTANGLE_WIDTH // CIRCLE_SIZE_TO_RECT_WIDTH)
CIRCLE_WIDTH, CIRCLE_HEIGHT = CIRCLE_SIZE, CIRCLE_SIZE

RECTANGLE_WIDTH_CAP = 650
SPEED_RATIO = 40
FALLING_SPEED = 19
BOTTOM_CIRCLE_RATIO = 1.20
BOTTOM_CIRCLE = HEIGHT // BOTTOM_CIRCLE_RATIO
FPS = 60
BLACK, DARK_PURPLE, PURPLE, PINK, WHITE = (0, 0, 0), (62, 5, 89), (104, 9, 148), (201, 160, 220), (255, 255, 255)
RECT_COMBO_DISPLAY = False
RECT_COLOR = PURPLE
MAX_CIRCLES_PER_FRAME = 30
INTERVAL_RATIO = 8
INTERVAL, KEY_DELAY = 180, 90
clock = time.Clock()
COMBO_DIVIDER = 10
LIFE_X, LIFE_Y = 50, 40

ACC_X_PADDING = 115
ACC_X, ACC_Y = WIDTH - ACC_X_PADDING, 60
SCORE_X_PADDING = 175
SCORE_X, SCORE_Y = WIDTH - SCORE_X_PADDING, 15

COMBO_Y_PADDING = 70
COMBO_X, COMBO_Y = 20, HEIGHT - COMBO_Y_PADDING
HIT_SOUNDS = True
NUM_OF_LANES = 4
MULTI_CIRCLE_CHANCE = 2
HIT_SOUND_VOLUME, MISS_SOUND_VOLUME = 0.2, 0.5
SONG_VOLUME = 1
END_SONG_DELAY = 2
MAX_LIFE, LIFE_DMG, OKAY_lIFE_DMG, LIFE_INCREASE = 100, 10, 5, 2
SONG_FADE = .1
SONG_FADE_MS = 100
IMPORT_MAP = False
UPDATE_MAP = True  # Not currently used
AUTO = False

ACC_Y_RATIO = 11.75
SCORE_X_RATIO = 4
ACC_X_RATIO = 6.09

LIFE_BAR_PADDING = 25
LIFE_BAR_Y_PADDING = 30
LIFE_BAR_HEIGHT_RATIO = 1.90
LIFE_BAR_COORDINATES = (
    WIDTH / 2 + (RECTANGLE_WIDTH / 2) + LIFE_BAR_PADDING, HEIGHT - LIFE_BAR_Y_PADDING, 10,
    HEIGHT // LIFE_BAR_HEIGHT_RATIO)

NAME_Y_RATIO = 3.02
NAME_Y = HEIGHT // NAME_Y_RATIO
NUM_OF_RECORD = 4
RECORD_Y_RATIO = 2.8
RECORD_Y = HEIGHT // RECORD_Y_RATIO
RECORD_Y_INTERVAL = 50
RECORD_Y_INTERVAL_RATIO = 14
RECORD_X = 20
SCORE_PADDING = 90
SCORE_PADDING_RATIO = 7.78
NAME_INTERVAL = 50

MID_COMBO_X, MID_COMBO_Y = 540, 300

PLAYER_NAME = "Kuriko"

RESIZABLE = True

ACC_IMG_SIZE = 80
ACC_IMG_X, ACC_IMG_Y = WIDTH / 2 - (ACC_IMG_SIZE / 2), HEIGHT // 2.3
ACC_IMG_WIDTH, ACC_IMG_HEIGHT = ACC_IMG_SIZE, ACC_IMG_SIZE

HIDE_PERFECT = False

CIRCLE_START_PADDING = 6 + RECTANGLE_WIDTH // 100
CIRCLE_X_START = RECTANGLE_X + CIRCLE_START_PADDING
BETWEEN_CIRCLE_PADDING = RECTANGLE_WIDTH // 4.25

LANES = {
    0: CIRCLE_X_START,
    1: CIRCLE_X_START + BETWEEN_CIRCLE_PADDING * 1,
    2: CIRCLE_X_START + BETWEEN_CIRCLE_PADDING * 2,
    3: CIRCLE_X_START + BETWEEN_CIRCLE_PADDING * 3,
}

MULTIPLE_CIRCLE_FREQ = {
    "2": 2,
    "3": 6,
    "4": 8
}

KEY_BINDS = {
    'pygame.K_a': 0,
    'pygame.K_s': 1,
    'pygame.K_k': 2,
    'pygame.K_l': 3,

}

ACC_CATEGORIES_POINTS = {
    "Okay": (50, 50),
    "Good": (75, 100),
    "Perfect": (100, 300),
    "Amazing": (100, 320)
}

FIRST_HIT_WINDOW, LAST_HIT_WINDOW = BOTTOM_CIRCLE - 60, BOTTOM_CIRCLE + 85
HIT_WINDOW_PADDING = (60, 85)

amazing_hit_window = (BOTTOM_CIRCLE + 10, BOTTOM_CIRCLE + 30)
perfect_hit_window = (amazing_hit_window[0] - 35, amazing_hit_window[1] + 35)
good_hit_window = (perfect_hit_window[0] - 15, perfect_hit_window[1] + 10)
okay_hit_window = (good_hit_window[0] - 10, good_hit_window[1] + 10)

AMAZING_SCORE_PADDING = (10, 30)
PERFECT_SCORE_PADDING = 35
GOOD_SCORE_PADDING = (15, 10)
OKAY_SCORE_PADDING = 10

ACC_CATEGORIES_HIT_WINDOW = {
    "Okay": okay_hit_window,
    "Good": good_hit_window,
    "Perfect": perfect_hit_window,
    "Amazing": amazing_hit_window
}

"""
Formula:
Okay = GOOD - 10 = 490, 625
GOOD = PERFECT - 15 = 500, 615
PERFECT = AMAZING - 35 = 515, 605
AMAZING = BOTTOM_CIRCLE + 10 + 20 = 550, 570

"""

GRADE_ACC = {
    "SS": 100,
    "S": 95.00,
    "A": 90.00,
    "B": 80.00,
    "C": 70.00,
    "D": 60.00,
}
