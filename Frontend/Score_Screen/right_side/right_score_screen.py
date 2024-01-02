from .text_button import TextButton
from .logo_grade import LogoGrade
from Frontend.Score_Screen.right_side.top_rect import TopRect
from Frontend.Helper_Files import ButtonEventHandler


class RightScoreScreen:
    def __init__(self, *, screen, pos, state, map_info):
        self.__text_button = TextButton(event_handler=ButtonEventHandler(), screen=screen, pos=pos,
                                        state=state)
        self.__top_rect = TopRect(pos=pos, map_info=map_info)
        self.__grade = LogoGrade(pos=pos)

    def show(self, screen, date_time: dict, grade: str):
        self.__text_button.show_text(screen=screen)
        self.__top_rect.show(screen=screen, date_time=date_time)
        self.__grade.show_grade(grade=grade, screen=screen)
