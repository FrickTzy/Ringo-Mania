from pygame import Rect, draw
from Frontend.settings import PURPLE, BLACK


class LifeBar:
    __LIFE_BAR_PADDING = 25
    __LIFE_BAR_Y_PADDING = 30
    __LIFE_BAR_HEIGHT_RATIO = 1.90

    def __init__(self, display):
        self.display = display
        x, y, width, height = self.life_bar_coordinates
        self.life_bar = Rect(x, y, width, height)

    def show_life_bar(self, life: int):
        self.update_life_bar_coord()
        draw.rect(self.display.window, PURPLE, self.life_bar_coordinates)
        draw.rect(self.display.window, BLACK, self.get_life_bar_height(life=life))

    @property
    def life_bar_coord_x(self):
        return self.display.width // 2 + (self.display.rectangle_width / 2) + self.__LIFE_BAR_PADDING

    @property
    def life_bar_coord_y(self):
        return self.display.height - self.__LIFE_BAR_Y_PADDING - self.__life_bar_height

    @property
    def __life_bar_height(self):
        return self.display.height // self.__LIFE_BAR_HEIGHT_RATIO

    @property
    def life_bar_coordinates(self) -> tuple[int, int, int, int]:
        return self.life_bar_coord_x, self.life_bar_coord_y, 10, self.__life_bar_height

    def get_life_bar_height(self, life):
        life_bar_height = int(self.life_bar.height * abs((life - 100) / 100))
        return self.life_bar.x - 1, self.life_bar.y, self.life_bar.width + 1, life_bar_height

    def update_life_bar_coord(self):
        self.life_bar.x = self.life_bar_coord_x
        self.life_bar.y = self.life_bar_coord_y
        self.life_bar.width = self.life_bar.width

