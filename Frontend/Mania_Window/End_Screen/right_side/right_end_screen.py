from .text_button import TextButton
from Frontend.Helper_Files import ButtonEventHandler


class RightEndScreen:
    def __init__(self, *, end_screen, pos, font, state):
        self.__text_button = TextButton(event_handler=ButtonEventHandler(), end_screen=end_screen, font=font, pos=pos,
                                        state=state)

    def show(self, end_screen):
        self.__text_button.show_text(end_screen=end_screen)
