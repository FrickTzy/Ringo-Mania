from pygame import Surface, SurfaceType
from Frontend.settings import WHITE


class AccText:
    def __init__(self, end_screen_surface: Surface | SurfaceType, screen_pos, opacity, font):
        self.__end_screen_surface = end_screen_surface
        self.__pos = StatsTextPos(screen_pos=screen_pos)
        self.__font = font
        self.__opacity = opacity

    def show_text(self, end_screen_surface, stats: dict) -> None:
        self.__update_surface(end_screen_surface=end_screen_surface)
        self.__font.update_font(height=self.__pos.height)
        self.__blit_stats(stats=stats["acc_dict"])
        self.__blit_combo_accuracy(combo=stats["highest_combo"], accuracy=stats["accuracy"])

    def __update_surface(self, end_screen_surface):
        self.__end_screen_surface = end_screen_surface

    def __blit_combo_accuracy(self, combo, accuracy):
        self.__show_combo(combo=combo)
        self.__show_accuracy(acc=accuracy)

    def __blit_stats(self, stats: dict):
        self.__show_perfect_acc(stats["Perfect"])
        self.__show_amazing_acc(stats["Amazing"])
        self.__show_okay_acc(stats["Okay"])
        self.__show_good_acc(stats["Good"])
        self.__show_misses(stats["Miss"])

    def __show_perfect_acc(self, acc) -> None:
        text = self.__font.font.render(f"{acc}x", True, WHITE)
        text.set_alpha(self.__opacity.opacity)
        self.__end_screen_surface.blit(text, self.__pos.left_text_pos(sequence_num=1))

    def __show_amazing_acc(self, acc) -> None:
        text = self.__font.font.render(f"{acc}x", True, WHITE)
        text.set_alpha(self.__opacity.opacity)
        self.__end_screen_surface.blit(text, self.__pos.right_text_pos(sequence_num=1))

    def __show_okay_acc(self, acc) -> None:
        text = self.__font.font.render(f"{acc}x", True, WHITE)
        text.set_alpha(self.__opacity.opacity)
        self.__end_screen_surface.blit(text, self.__pos.left_text_pos(sequence_num=2))

    def __show_good_acc(self, acc) -> None:
        text = self.__font.font.render(f"{acc}x", True, WHITE)
        text.set_alpha(self.__opacity.opacity)
        self.__end_screen_surface.blit(text, self.__pos.right_text_pos(sequence_num=2))

    def __show_misses(self, acc) -> None:
        text = self.__font.font.render(f"{acc}x", True, WHITE)
        text.set_alpha(self.__opacity.opacity)
        self.__end_screen_surface.blit(text, self.__pos.center_pos(sequence_num=3))

    def __show_combo(self, combo) -> None:
        text = self.__font.font.render(f"{combo}x", True, WHITE)
        text.set_alpha(self.__opacity.opacity)
        self.__end_screen_surface.blit(text, self.__pos.combo_text_pos())

    def __show_accuracy(self, acc) -> None:
        text = self.__font.font.render(f"{acc}", True, WHITE)
        text.set_alpha(self.__opacity.opacity)
        if self.__check_if_acc_is_small(acc=acc):
            self.__end_screen_surface.blit(text, self.__pos.small_acc_text_pos())
        else:
            self.__end_screen_surface.blit(text, self.__pos.acc_text_pos())

    @staticmethod
    def __check_if_acc_is_small(acc: str) -> bool:
        if float(acc.removesuffix("%")) < 10.00:
            return True
        return False


class StatsTextPos:
    __LEFT_X_RATIO = 8.1
    __RIGHT_X_RATIO = 2.94
    __CENTER_X_RATIO = 4.65
    __Y_START_RATIO = 4.50
    __Y_INTERVAL_RATIO = 5.50
    __COMBO_X_RATIO = 14.55
    __ACC_X_RATIO = 3.69
    __SMALL_ACC_X_RATIO = 3.39
    __BOTTOM_TEXT_Y_RATIO = 1.18

    def __init__(self, screen_pos):
        self.screen_pos = screen_pos

    def left_text_pos(self, sequence_num: int) -> tuple[int, int]:
        return self.__left_x, self.__y_start + (sequence_num - 1) * self.__y_interval

    def right_text_pos(self, sequence_num: int) -> tuple[int, int]:
        return self.__right_x, self.__y_start + (sequence_num - 1) * self.__y_interval

    def combo_text_pos(self) -> tuple[int, int]:
        return self.__combo_x, self.__bottom_text_y

    def acc_text_pos(self) -> tuple[int, int]:
        return self.__acc_x, self.__bottom_text_y

    def small_acc_text_pos(self) -> tuple[int, int]:
        return self.__small_acc_x, self.__bottom_text_y

    def center_pos(self, sequence_num: int) -> tuple[int, int]:
        return self.__center_x, self.__y_start + (sequence_num - 1) * self.__y_interval

    @property
    def __bottom_text_y(self):
        return self.screen_pos.height // self.__BOTTOM_TEXT_Y_RATIO

    @property
    def __combo_x(self):
        return self.screen_pos.width // self.__COMBO_X_RATIO

    @property
    def __acc_x(self):
        return self.screen_pos.width // self.__ACC_X_RATIO

    @property
    def __small_acc_x(self):
        return self.screen_pos.width // self.__SMALL_ACC_X_RATIO

    @property
    def __left_x(self):
        return self.screen_pos.width // self.__LEFT_X_RATIO

    @property
    def __right_x(self):
        return self.screen_pos.width // self.__RIGHT_X_RATIO

    @property
    def __center_x(self):
        return self.screen_pos.width // self.__CENTER_X_RATIO

    @property
    def __y_start(self):
        return self.screen_pos.height // self.__Y_START_RATIO

    @property
    def __y_interval(self):
        return self.screen_pos.height // self.__Y_INTERVAL_RATIO

    @property
    def height(self):
        return self.screen_pos.height
