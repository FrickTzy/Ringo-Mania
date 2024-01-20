from pygame import Surface, SurfaceType
from Frontend.Settings import Color
from pygame import font
from .combo_acc import ComboAcc


class AccText:
    __COLOR = Color.WHITE

    def __init__(self, screen_surface: Surface | SurfaceType, screen_pos, opacity):
        self.__screen_surface = screen_surface
        self.__pos = StatsTextPos(screen_pos=screen_pos)
        self.__font = Font()
        self.__opacity = opacity
        self.__combo_acc = ComboAcc(pos=screen_pos)

    def show_text(self, screen_surface, stats: dict) -> None:
        self.__update_surface(screen_surface=screen_surface)
        self.__font.update_font(height=self.__pos.height)
        self.__blit_score(score=stats["score"])
        self.__blit_stats(stats=stats["acc_dict"])
        self.__combo_acc.show(screen=screen_surface, acc=stats["accuracy"], combo=stats["highest_combo"])

    def __update_surface(self, screen_surface):
        self.__screen_surface = screen_surface

    def __blit_score(self, score: int):
        text = self.__font.score_font.render(f"{score}", True, self.__COLOR)
        score_label = self.__font.score_label_font.render("Score", True, self.__COLOR)
        text.set_alpha(self.__opacity.opacity)
        self.__screen_surface.blit(score_label, self.__pos.score_label_pos)
        self.__screen_surface.blit(text, self.__pos.score_pos)

    def __blit_stats(self, stats: dict):
        self.__show_perfect_acc(stats["Perfect"])
        self.__show_amazing_acc(stats["Amazing"])
        self.__show_okay_acc(stats["Okay"])
        self.__show_good_acc(stats["Good"])
        self.__show_misses(stats["Miss"])

    def __show_perfect_acc(self, acc) -> None:
        text = self.__font.font.render(f"{acc}x", True, self.__COLOR)
        text.set_alpha(self.__opacity.opacity)
        self.__screen_surface.blit(text, self.__pos.left_text_pos(sequence_num=1))

    def __show_amazing_acc(self, acc) -> None:
        text = self.__font.font.render(f"{acc}x", True, self.__COLOR)
        text.set_alpha(self.__opacity.opacity)
        self.__screen_surface.blit(text, self.__pos.right_text_pos(sequence_num=1))

    def __show_okay_acc(self, acc) -> None:
        text = self.__font.font.render(f"{acc}x", True, self.__COLOR)
        text.set_alpha(self.__opacity.opacity)
        self.__screen_surface.blit(text, self.__pos.left_text_pos(sequence_num=2))

    def __show_good_acc(self, acc) -> None:
        text = self.__font.font.render(f"{acc}x", True, self.__COLOR)
        text.set_alpha(self.__opacity.opacity)
        self.__screen_surface.blit(text, self.__pos.right_text_pos(sequence_num=2))

    def __show_misses(self, acc) -> None:
        text = self.__font.font.render(f"{acc}x", True, self.__COLOR)
        text.set_alpha(self.__opacity.opacity)
        self.__screen_surface.blit(text, self.__pos.center_pos(sequence_num=3))


class Font:
    __FONT_RATIO = 15
    __SCORE_FONT_RATIO = 20
    __SCORE_LABEL_RATIO = 40

    def __init__(self):
        self.font = font.SysFont("arialblack", 15, bold=True)
        self.score_font = font.SysFont("arialblack", 15, bold=True)
        self.score_label_font = font.SysFont("arialblack", 12, bold=True)

    def update_font(self, height: int):
        self.font = font.SysFont("arialblack", self.__font_size(height=height))
        self.score_font = font.SysFont("arialblack", self.__score_size(height=height))
        self.score_label_font = font.SysFont("arialblack", self.__score_label_size(height=height))

    def __font_size(self, height: int):
        return height // self.__FONT_RATIO

    def __score_size(self, height: int):
        return height // self.__SCORE_FONT_RATIO

    def __score_label_size(self, height: int):
        return height // self.__SCORE_LABEL_RATIO

    def text_size(self, text: str) -> tuple[int, int]:
        width, height = self.font.size(text)
        return width, height


class StatsTextPos:
    __LEFT_X_RATIO = 8.1
    __RIGHT_X_RATIO = 2.94
    __CENTER_X_RATIO = 4.65
    __Y_START_RATIO = 4.50
    __Y_INTERVAL_RATIO = 5.50
    __SCORE_X_RATIO, __SCORE_Y_RATIO = 21.62, 25.69
    __SCORE_LABEL_X_RATIO, __SCORE_LABEL_Y_RATIO = 32, 69.23

    def __init__(self, screen_pos):
        self.screen_pos = screen_pos

    @property
    def score_pos(self) -> tuple[int, int]:
        return self.__score_x, self.__score_y

    @property
    def score_label_pos(self) -> tuple[int, int]:
        return self.__score_label_x, self.__score_label_y

    def left_text_pos(self, sequence_num: int) -> tuple[int, int]:
        return self.__left_x, self.__y_start + (sequence_num - 1) * self.__y_interval

    def right_text_pos(self, sequence_num: int) -> tuple[int, int]:
        return self.__right_x, self.__y_start + (sequence_num - 1) * self.__y_interval

    def center_pos(self, sequence_num: int) -> tuple[int, int]:
        return self.__center_x, self.__y_start + (sequence_num - 1) * self.__y_interval

    @property
    def __score_x(self):
        return self.screen_pos.width // self.__SCORE_X_RATIO

    @property
    def __score_y(self):
        return self.screen_pos.height // self.__SCORE_Y_RATIO

    @property
    def __score_label_x(self):
        return self.screen_pos.width // self.__SCORE_LABEL_X_RATIO

    @property
    def __score_label_y(self):
        return self.screen_pos.height // self.__SCORE_LABEL_Y_RATIO

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
