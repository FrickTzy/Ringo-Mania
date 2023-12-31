from .text_button import TextButton
from .logo_grade import LogoGrade
from Frontend.Mania_Window.End_Screen.right_side.top_rect.top_rect import TopRect
from Frontend.Helper_Files import ButtonEventHandler


class RightEndScreen:
    def __init__(self, *, end_screen, pos, state, map_info):
        self.__text_button = TextButton(event_handler=ButtonEventHandler(), end_screen=end_screen, pos=pos,
                                        state=state)
        self.__top_rect = TopRect(pos=pos, map_info=map_info)
        self.__grade = LogoGrade(pos=pos)

    def show(self, end_screen, date_time: dict, grade: str):
        self.__text_button.show_text(end_screen=end_screen)
        self.__top_rect.show(end_screen=end_screen, date_time=date_time)
        self.__grade.show_grade(grade=grade, end_screen=end_screen)
