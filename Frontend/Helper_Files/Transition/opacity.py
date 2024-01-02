class Opacity:
    __OPACITY_INTERVAL = 5

    def __init__(self, opacity: int = 0):
        self.__opacity = opacity

    @property
    def opacity(self) -> int:
        if self.__opacity > 255:
            self.__opacity = 255
        return self.__opacity

    @property
    def max_opacity(self) -> bool:
        return self.opacity == 255

    @property
    def min_opacity(self) -> bool:
        return self.__opacity <= 0

    def reset_opacity(self) -> None:
        self.__opacity = 0

    def set_opacity(self, opacity: int):
        self.__opacity = opacity

    def subtract_opacity(self, subtract_num: int = 5) -> None:
        if self.__opacity > 0:
            self.__opacity -= subtract_num

    def add_opacity(self, sum_num: int = 5) -> None:
        if self.__opacity < 255:
            self.__opacity += sum_num
