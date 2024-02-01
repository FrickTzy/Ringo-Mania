from pygame import font
from Frontend.Settings import Color


class PlayTimeText:
    __COLOR = Color.WHITE

    def __init__(self, pos):
        self.__pos = PlayTimeTextPos(pos=pos)
        self.__font = Font()

    def show(self, screen, date_time: dict):
        self.__font.check_if_update_font(height=self.__pos.height)
        self.__show_text(screen=screen, date_time=date_time)

    def __show_text(self, screen, date_time: dict):
        time_text = self.__font.date_time_font.render(f"Played on {date_time['time']} - {date_time['date']}", True,
                                                      self.__COLOR)
        screen.blit(time_text, self.__pos.date_time_pos)


class PlayTimeTextPos:
    __X_TEXT_RATIO, __Y_TEXT_RATIO = 1.28, 7.6

    def __init__(self, pos):
        self.__pos = pos

    @property
    def date_time_pos(self):
        return self.__x_pos, self.__y_pos

    @property
    def __x_pos(self):
        return self.__pos.width // self.__X_TEXT_RATIO

    @property
    def __y_pos(self):
        return self.__pos.height // self.__Y_TEXT_RATIO

    @property
    def height(self):
        return self.__pos.height


class Font:
    __TIME_FONT_RATIO = 50
    __current_height = 0

    def __init__(self):
        self.__date_time_font = font.SysFont("Arialblack", 20)

    @property
    def date_time_font(self):
        return self.__date_time_font

    def __update_font(self, height: int):
        self.__date_time_font = font.SysFont("Arialblack", self.__time_font_size(height=height))

    def check_if_update_font(self, height: int):
        if self.__current_height == height:
            return
        self.__update_font(height=height)
        self.__current_height = height

    def __time_font_size(self, height: int):
        return height // self.__TIME_FONT_RATIO
