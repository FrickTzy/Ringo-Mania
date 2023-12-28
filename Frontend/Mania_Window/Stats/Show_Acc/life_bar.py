from pygame import Rect, draw
from Frontend.settings import PURPLE, BLACK


class LifeBar:
    __LIFE_BAR_PADDING = 25
    __LIFE_BAR_Y_PADDING = 30
    __LIFE_BAR_HEIGHT_RATIO = 1.90

    def __init__(self, display, rectangle_pos):
        self.__display = display
        self.__rectangle_pos = rectangle_pos
        x, y, width, height = self.__life_bar_coordinates
        self.__life_bar = Rect(x, y, width, height)

    def show_life_bar(self, life: int):
        self.update_life_bar_coord()
        draw.rect(self.__display.window, PURPLE, self.__life_bar_coordinates)
        draw.rect(self.__display.window, BLACK, self.get_life_bar_height(life=life))

    @property
    def __life_bar_coord_x(self):
        return self.__display.width // 2 + (self.__rectangle_pos.rectangle_width / 2) + self.__LIFE_BAR_PADDING

    @property
    def __life_bar_coord_y(self):
        return self.__display.height - self.__LIFE_BAR_Y_PADDING - self.__life_bar_height

    @property
    def __life_bar_height(self):
        return self.__display.height // self.__LIFE_BAR_HEIGHT_RATIO

    @property
    def __life_bar_coordinates(self) -> tuple[int, int, int, int]:
        return self.__life_bar_coord_x, self.__life_bar_coord_y, 10, self.__life_bar_height

    def get_life_bar_height(self, life):
        life_bar_height = int(self.__life_bar.height * abs((life - 100) / 100))
        return self.__life_bar.x - 1, self.__life_bar.y, self.__life_bar.width + 1, life_bar_height

    def update_life_bar_coord(self):
        self.__life_bar.x = self.__life_bar_coord_x
        self.__life_bar.y = self.__life_bar_coord_y
        self.__life_bar.width = self.__life_bar.width
