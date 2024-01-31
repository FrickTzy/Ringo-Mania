from Frontend.Score_Screen.button_font import ButtonFont
from Frontend.Settings import Color


class TextButton:
    __CONTINUE = "Continue"
    __COLOR = Color.WHITE

    def __init__(self, event_handler, screen, pos, state):
        self.__event_handler = event_handler
        self.__font = ButtonFont()
        self.__screen = screen
        self.__pos = ButtonPos(pos=pos)
        self.__state = state

    def show_text(self, screen) -> None:
        self.__update_surface(screen=screen)
        self.__font.check_if_update_font(height=self.__pos.height)
        self.__run_text()

    def __update_surface(self, screen):
        self.__screen = screen

    def __run_text(self):
        self.__run_continue_text(command=lambda: self.__state.leave_score_screen())

    def __run_continue_text(self, command) -> None:
        text = self.__font.font.render(self.__CONTINUE, True, self.__COLOR)
        self.__screen.blit(text, self.__pos.continue_pos)
        self.__event_handler.check_buttons_for_clicks(starting_pos=self.__pos.continue_pos,
                                                      size=self.__font.text_size(text=self.__CONTINUE),
                                                      command=command)


class ButtonPos:
    __CONTINUE_X_RATIO, __CONTINUE_Y_RATIO = 1.31, 1.2

    def __init__(self, pos):
        self.__pos = pos

    @property
    def continue_pos(self):
        return self.__continue_x, self.__continue_y

    @property
    def height(self):
        return self.__pos.height

    @property
    def __continue_x(self):
        return self.__pos.width // self.__CONTINUE_X_RATIO

    @property
    def __continue_y(self):
        return self.__pos.height // self.__CONTINUE_Y_RATIO
