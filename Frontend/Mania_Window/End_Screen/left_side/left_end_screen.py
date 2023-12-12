from .acc_text import AccText
from .acc_logo import AccLogo


class LeftEndScreen:
    def __init__(self, *, opacity, end_screen, pos):
        self.__acc_text = AccText(end_screen_surface=end_screen, screen_pos=pos,
                                  opacity=opacity)
        self.__acc_logo = AccLogo(screen_pos=pos, opacity=opacity)

    def show(self, end_screen, stats):
        self.__acc_text.show_text(end_screen_surface=end_screen, stats=stats)
        self.__acc_logo.show_logo(end_screen_surface=end_screen)
