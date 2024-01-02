from pygame import font


class ButtonFont:
    __FONT_RATIO = 23

    def __init__(self):
        self.font = font.SysFont("Roboto", 15, bold=True)

    def update_font(self, height: int):
        size = int(height // self.__FONT_RATIO)
        self.font = font.SysFont("arialblack", size)

    def text_size(self, text: str) -> tuple[int, int]:
        width, height = self.font.size(text)
        return width, height
