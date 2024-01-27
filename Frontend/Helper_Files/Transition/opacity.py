class Opacity:
    __OPACITY_INTERVAL = 5
    __MAX_OPACITY = 255

    def __init__(self, opacity: int = 0):
        self.__opacity = opacity

    @property
    def opacity(self) -> int:
        if self.__opacity > self.__MAX_OPACITY:
            self.__opacity = self.__MAX_OPACITY
        return self.__opacity

    @property
    def max_opacity(self) -> bool:
        return self.opacity == self.__MAX_OPACITY

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
        if self.__opacity < self.__MAX_OPACITY:
            self.__opacity += sum_num

    def set_opacity_by_percentage(self, percentage: float):
        self.__opacity = self.__get_opacity_by_percentage(percentage=percentage)

    def subtract_opacity_by_percentage(self, percentage) -> None:
        if self.__opacity > 0:
            self.__opacity = self.__MAX_OPACITY - self.__get_opacity_by_percentage(percentage=percentage)

    def __get_opacity_by_percentage(self, percentage: float):
        return int(percentage * self.__MAX_OPACITY)
