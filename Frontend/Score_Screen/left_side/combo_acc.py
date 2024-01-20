from pygame import font
from Frontend.Settings import Color


class ComboAcc:
    __COLOR = Color.WHITE

    def __init__(self, pos):
        self.__pos = Pos(pos=pos)
        self.__font = Font()

    def show(self, screen, combo, acc):
        self.__show_combo(screen=screen, combo=combo)
        self.__show_accuracy(screen=screen, acc=acc)

    def __show_combo(self, screen, combo) -> None:
        text = self.__font.font(height=self.__pos.height).render(f"{combo}x", True, self.__COLOR)
        label = self.__font.label_font(height=self.__pos.height).render("Combo", True, self.__COLOR)
        screen.blit(text, self.__pos.combo_text_pos)
        screen.blit(label, self.__pos.combo_label_pos)

    def __show_accuracy(self, screen, acc) -> None:
        text = self.__font.font(height=self.__pos.height).render(f"{acc}", True, self.__COLOR)
        label = self.__font.label_font(height=self.__pos.height).render("Acc", True, self.__COLOR)
        screen.blit(label, self.__pos.acc_label_pos)
        if self.__check_if_acc_is_small(acc=acc):
            screen.blit(text, self.__pos.small_acc_text_pos())
        else:
            screen.blit(text, self.__pos.acc_text_pos())

    @staticmethod
    def __check_if_acc_is_small(acc: str) -> bool:
        if float(acc.removesuffix("%")) < 10.00:
            return True
        return False


class Pos:
    __BOTTOM_TEXT_Y_RATIO = 1.16
    __COMBO_X_RATIO = 14.55
    __ACC_X_RATIO = 3.6
    __SMALL_ACC_X_RATIO = 3.48
    __COMBO_LABEL_X_RATIO = 17.78
    __ACC_LABEL_X_RATIO = 3.81
    __LABEL_Y_RATIO = 1.2

    def __init__(self, pos):
        self.__pos = pos

    @property
    def combo_text_pos(self) -> tuple[int, int]:
        return self.__combo_x, self.__bottom_text_y

    @property
    def combo_label_pos(self) -> tuple[int, int]:
        return self.__combo_label_x, self.__label_y

    @property
    def acc_label_pos(self) -> tuple[int, int]:
        return self.__acc_label_x, self.__label_y

    def acc_text_pos(self) -> tuple[int, int]:
        return self.__acc_x, self.__bottom_text_y

    def small_acc_text_pos(self) -> tuple[int, int]:
        return self.__small_acc_x, self.__bottom_text_y

    @property
    def __combo_label_x(self):
        return self.__pos.width // self.__COMBO_LABEL_X_RATIO

    @property
    def __acc_label_x(self):
        return self.__pos.width // self.__ACC_LABEL_X_RATIO

    @property
    def __label_y(self):
        return self.__pos.height // self.__LABEL_Y_RATIO

    @property
    def __acc_x(self):
        return self.__pos.width // self.__ACC_X_RATIO

    @property
    def __small_acc_x(self):
        return self.__pos.width // self.__SMALL_ACC_X_RATIO

    @property
    def __bottom_text_y(self):
        return self.__pos.height // self.__BOTTOM_TEXT_Y_RATIO

    @property
    def __combo_x(self):
        return self.__pos.width // self.__COMBO_X_RATIO

    @property
    def height(self):
        return self.__pos.height


def combo_text_pos(self) -> tuple[int, int]:
    return self.__combo_x, self.__bottom_text_y


class Font:
    __FONT_RATIO = 16
    __LABEL_RATIO = 35

    def font(self, height):
        return font.SysFont("arialblack", self.__font_size(height=height))

    def label_font(self, height):
        return font.SysFont("arialblack", self.__label_size(height=height))

    def __font_size(self, height: int):
        return height // self.__FONT_RATIO

    def __label_size(self, height: int):
        return height // self.__LABEL_RATIO
