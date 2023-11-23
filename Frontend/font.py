from pygame import font


class Font:
    __RECORD_TEXT_RATIO = 63.64
    __MAIN_FONT_RATIO = 24.14
    __ACC_FONT_RATIO = 30.43

    def __init__(self):
        self.record_font = font.SysFont("arialblack", 10)
        self.acc_font = font.SysFont("arialblack", 12)
        self.main_font = font.SysFont("arialblack", 12)

    def update_all_font(self, height: int) -> None:
        self.change_record_font_size(height)
        self.change_main_font_size(height)
        self.change_acc_font_size(height)

    def change_record_font_size(self, height: int) -> None:
        size = int(height // self.__RECORD_TEXT_RATIO)
        self.record_font = font.SysFont("arialblack", size)

    def change_main_font_size(self, height: int) -> None:
        size = int(height // self.__MAIN_FONT_RATIO)
        self.main_font = font.SysFont("arialblack", size)

    def change_acc_font_size(self, height: int) -> None:
        size = int(height // self.__ACC_FONT_RATIO)
        self.acc_font = font.SysFont("arialblack", size)
