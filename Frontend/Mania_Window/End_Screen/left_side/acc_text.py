from pygame import Surface, SurfaceType
from Frontend.settings import WHITE


class AccText:
    def __init__(self, end_screen_surface: Surface | SurfaceType, screen_pos, font, opacity):
        self.__end_screen_surface = end_screen_surface
        self.__pos = StatsTextPos(screen_pos=screen_pos)
        self.__font = font
        self.__opacity = opacity

    def show_text(self, end_screen_surface, stats: dict) -> None:
        self.__update_surface(end_screen_surface=end_screen_surface)
        self.__blit_text(stats=stats)

    def __update_surface(self, end_screen_surface):
        self.__end_screen_surface = end_screen_surface

    def __blit_text(self, stats: dict):
        self.__show_perfect_acc(stats["Perfect"])
        self.__show_amazing_acc(stats["Amazing"])
        self.__show_okay_acc(stats["Okay"])

    def __show_perfect_acc(self, acc) -> None:
        text = self.__font.main_pause_font.render(f"{acc}x", True, WHITE)
        text.set_alpha(self.__opacity.opacity)
        self.__end_screen_surface.blit(text, self.__pos.left_text_pos(sequence_num=1))

    def __show_amazing_acc(self, acc) -> None:
        text = self.__font.main_pause_font.render(f"{acc}x", True, WHITE)
        text.set_alpha(self.__opacity.opacity)
        self.__end_screen_surface.blit(text, self.__pos.right_text_pos(sequence_num=1))

    def __show_okay_acc(self, acc) -> None:
        text = self.__font.main_pause_font.render(f"{acc}x", True, WHITE)
        text.set_alpha(self.__opacity.opacity)
        self.__end_screen_surface.blit(text, self.__pos.left_text_pos(sequence_num=2))


class StatsTextPos:
    __Y_INTERVAL = 200

    def __init__(self, screen_pos):
        self.screen_pos = screen_pos

    def left_text_pos(self, sequence_num: int) -> tuple[int, int]:
        return 200, sequence_num * self.__Y_INTERVAL

    def right_text_pos(self, sequence_num: int) -> tuple[int, int]:
        return 550, sequence_num * self.__Y_INTERVAL
