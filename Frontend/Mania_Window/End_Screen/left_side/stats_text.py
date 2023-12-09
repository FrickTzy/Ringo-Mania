from pygame import Surface, SurfaceType
from Frontend.settings import WHITE


class StatsText:
    __PERFECT_TEXT = "Perfect"

    def __init__(self, end_screen_surface: Surface | SurfaceType, screen_pos, font, opacity):
        self.__end_screen_surface = end_screen_surface
        self.__pos = StatsTextPos(screen_pos=screen_pos)
        self.__font = font
        self.__opacity = opacity

    def show_text(self, end_screen_surface) -> None:
        self.__update_surface(end_screen_surface=end_screen_surface)
        self.__blit_text()

    def __update_surface(self, end_screen_surface):
        self.__end_screen_surface = end_screen_surface

    def __blit_text(self):
        self.__show_perfect_acc()

    def __show_perfect_acc(self) -> None:
        text = self.__font.main_pause_font.render(self.__PERFECT_TEXT, True, WHITE)
        text.set_alpha(self.__opacity.opacity)
        self.__end_screen_surface.blit(text, self.__pos.left_text_pos)


class StatsTextPos:
    def __init__(self, screen_pos):
        self.screen_pos = screen_pos

    @property
    def left_text_pos(self) -> tuple[int, int]:
        return 200, 200
