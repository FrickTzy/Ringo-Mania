from pygame import Surface, SurfaceType, font
from Frontend.settings import WHITE


class AccText:
    def __init__(self, end_screen_surface: Surface | SurfaceType, screen_pos, opacity):
        self.__end_screen_surface = end_screen_surface
        self.__pos = StatsTextPos(screen_pos=screen_pos)
        self.__font = EndScreenFont()
        self.__opacity = opacity

    def show_text(self, end_screen_surface, stats: dict) -> None:
        self.__update_surface(end_screen_surface=end_screen_surface)
        self.__font.update_font(height=self.__pos.height)
        self.__blit_text(stats=stats)

    def __update_surface(self, end_screen_surface):
        self.__end_screen_surface = end_screen_surface

    def __blit_text(self, stats: dict):
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
        self.__end_screen_surface.blit(text, self.__pos.center_pos())


class StatsTextPos:
    __Y_INTERVAL = 200

    def __init__(self, screen_pos):
        self.screen_pos = screen_pos

    def left_text_pos(self, sequence_num: int) -> tuple[int, int]:
        return 200, sequence_num * self.__Y_INTERVAL

    def right_text_pos(self, sequence_num: int) -> tuple[int, int]:
        return 550, sequence_num * self.__Y_INTERVAL

    def center_pos(self):
        return 350, 3 * self.__Y_INTERVAL

    @property
    def height(self):
        return self.screen_pos.height


class EndScreenFont:
    __FONT_RATIO = 13

    def __init__(self):
        self.font = font.SysFont("arialblack", 15)

    def update_font(self, height: int):
        size = int(height // self.__FONT_RATIO)
        self.font = font.SysFont("arialblack", size)
