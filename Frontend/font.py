from pygame import font


class Font:
    __RECORD_TEXT_RATIO = 63.64
    __MAIN_FONT_RATIO = 24.14
    __PAUSE_FONT_RATIO = 21
    __MAIN_PAUSE_FONT_RATIO = 14
    __ACC_FONT_RATIO = 30.43

    def __init__(self):
        self.record_font = font.SysFont("arialblack", 10)
        self.acc_font = font.SysFont("arialblack", 12)
        self.main_font = font.SysFont("arialblack", 12)
        self.pause_font = font.SysFont("arialblack", 15)
        self.main_pause_font = font.SysFont("arialblack", 17)

    def update_all_font(self, height: int) -> None:
        self.change_record_font_size(height)
        self.change_main_font_size(height)
        self.change_acc_font_size(height)
        self.change_pause_font_size(height)
        self.change_main_pause_font_size(height)

    def change_record_font_size(self, height: int) -> None:
        size = int(height // self.__RECORD_TEXT_RATIO)
        self.record_font = font.SysFont("arialblack", size)

    def change_main_font_size(self, height: int) -> None:
        size = int(height // self.__MAIN_FONT_RATIO)
        self.main_font = font.SysFont("arialblack", size)

    def change_acc_font_size(self, height: int) -> None:
        size = int(height // self.__ACC_FONT_RATIO)
        self.acc_font = font.SysFont("arialblack", size)

    def change_pause_font_size(self, height: int) -> None:
        size = int(height // self.__PAUSE_FONT_RATIO)
        self.pause_font = font.SysFont("arialblack", size)

    def change_main_pause_font_size(self, height: int) -> None:
        size = int(height // self.__MAIN_PAUSE_FONT_RATIO)
        self.main_pause_font = font.SysFont("arialblack", size)

    def get_text_center_coord(self, coord: tuple[int, int], font_type: str, text: str) -> tuple[int, int]:
        width, height = coord
        return (width // 2) - int(self.pause_text_width(font_type=font_type, text=text) / 2), int(height / 2.9)

    def get_text_x(self, font_type: str, text: str, width: int):
        return (width // 2) - (self.pause_text_width(font_type, text) / 2)

    def pause_text_size(self, font_type: str, text: str) -> tuple[int, int]:
        width, height = eval(f"self.{font_type}.size(text)")
        return width, height

    def pause_text_width(self, font_type: str, text: str) -> int:
        width, height = self.pause_text_size(font_type, text)
        return width
