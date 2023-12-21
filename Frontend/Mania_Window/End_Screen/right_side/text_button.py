from pygame import mouse, font
from Frontend.settings import WHITE


class TextButton:
    __CONTINUE = "Continue"
    __RESTART = "Restart"
    __COLOR = WHITE

    def __init__(self, event_handler, end_screen, pos, state):
        self.__event_handler = event_handler
        self.__font = ButtonFont()
        self.__end_screen = end_screen
        self.__pos = ButtonPos(pos=pos)
        self.__state = state

    def show_text(self, end_screen) -> None:
        self.__update_surface(end_screen=end_screen)
        self.__font.update_font(height=self.__pos.height)
        self.__run_text()

    def __update_surface(self, end_screen):
        self.__end_screen = end_screen

    def __run_text(self):
        self.__run_continue_text(command=lambda: quit())
        self.__run_restart_text(command=lambda: self.__restart())

    def __run_continue_text(self, command) -> None:
        text = self.__font.font.render(self.__CONTINUE, True, WHITE)
        self.__end_screen.blit(text, self.__pos.continue_pos)
        self.__event_handler.check_buttons_for_clicks(starting_pos=self.__pos.continue_pos,
                                                      text_size=self.__font.text_size(text=self.__CONTINUE),
                                                      command=command)

    def __run_restart_text(self, command) -> None:
        text = self.__font.font.render(self.__RESTART, True, WHITE)
        self.__end_screen.blit(text, self.__pos.restart_pos)
        self.__event_handler.check_buttons_for_clicks(starting_pos=self.__pos.restart_pos,
                                                      text_size=self.__font.text_size(text=self.__RESTART),
                                                      command=command)

    def __restart(self):
        self.__state.restart()
        mouse.set_visible(False)


class ButtonPos:
    __CONTINUE_X_RATIO = 1.31
    __RESTART_X_RATIO = 1.30
    __CONTINUE_Y_RATIO = 1.2
    _RESTART_Y_RATIO = 1.1

    def __init__(self, pos):
        self.__pos = pos

    @property
    def continue_pos(self):
        return self.__continue_x, self.__continue_y

    @property
    def restart_pos(self):
        return self.__restart_x, self.__restart_y

    @property
    def height(self):
        return self.__pos.height

    @property
    def __continue_x(self):
        return self.__pos.width // self.__CONTINUE_X_RATIO

    @property
    def __restart_x(self):
        return self.__pos.width // self.__RESTART_X_RATIO

    @property
    def __continue_y(self):
        return self.__pos.height // self.__CONTINUE_Y_RATIO

    @property
    def __restart_y(self):
        return self.__pos.height // self._RESTART_Y_RATIO


class ButtonFont:
    __FONT_RATIO = 23

    def __init__(self):
        self.font = font.SysFont("Roboto", 15, bold=True)

    def update_font(self, height: int):
        size = int(height // self.__FONT_RATIO)
        self.font = font.SysFont("arialblack", size)

    def text_size(self, text: str) -> tuple[int, int]:
        width, height = self.font.size(text)
        return width, height
