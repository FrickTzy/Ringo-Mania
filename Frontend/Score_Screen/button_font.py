from pygame import font


class ButtonFont:
    __FONT_RATIO = 23
    __current_height = 0

    def __init__(self):
        self.__font = font.SysFont("Roboto", 15, bold=True)

    def __update_font(self, height: int):
        size = int(height // self.__FONT_RATIO)
        self.__font = font.SysFont("arialblack", size)

    def check_if_update_font(self, height: int):
        if self.__current_height == height:
            return
        self.__update_font(height=height)
        self.__current_height = height

    def text_size(self, text: str) -> tuple[int, int]:
        width, height = self.__font.size(text)
        return width, height

    @property
    def font(self):
        return self.__font
