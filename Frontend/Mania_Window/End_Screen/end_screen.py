from pygame import Surface, SurfaceType

from Frontend.Score_Screen import ScoreScreen
from Frontend.Helper_Files import ButtonEventHandler

from .restart_button import RestartButton


class EndScreen(ScoreScreen):
    __SHOW_BACKGROUND = True

    def __init__(self, window_size: tuple[int, int], state, map_info):
        super().__init__(window_size=window_size, state=state, map_info=map_info)
        self.__restart_button = RestartButton(event_handler=ButtonEventHandler(), end_screen=self.score_screen,
                                              pos=self.pos, state=state)

    def show_end_screen(self, window: SurfaceType | Surface, size: tuple[int, int], stats: dict, date_time: dict,
                        grade):
        if self.fade_effect.finished_fade_in:
            self.show_screen(size=size, stats=stats, date_time=date_time, grade=grade)
            self.__restart_button.show_text(end_screen=self.score_screen)
            window.blit(self.score_screen, (0, 0))
        self.finished_delay_and_fade(window=window, has_delay=True)
