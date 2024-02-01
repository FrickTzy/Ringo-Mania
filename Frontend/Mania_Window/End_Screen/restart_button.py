from pygame import mouse
from Frontend.Settings import Color
from Frontend.Score_Screen.button_font import ButtonFont


class RestartButton:
    __RESTART = "Restart"
    __COLOR = Color.WHITE

    def __init__(self, event_handler, end_screen, pos, state):
        self.__event_handler = event_handler
        self.__font = ButtonFont()
        self.__end_screen = end_screen
        self.__pos = ButtonPos(pos=pos)
        self.__state = state

    def show_text(self, end_screen) -> None:
        self.__update_surface(end_screen=end_screen)
        self.__font.check_if_update_font(height=self.__pos.height)
        self.__run_text()

    def __update_surface(self, end_screen):
        self.__end_screen = end_screen

    def __run_text(self):
        self.__run_restart_text(command=lambda: self.__restart())

    def __run_restart_text(self, command) -> None:
        text = self.__font.font.render(self.__RESTART, True, self.__COLOR)
        self.__end_screen.blit(text, self.__pos.restart_pos)
        self.__event_handler.check_buttons_for_clicks(starting_pos=self.__pos.restart_pos,
                                                      size=self.__font.text_size(text=self.__RESTART),
                                                      command=command)

    def __restart(self):
        self.__state.restart()
        mouse.set_visible(False)


class ButtonPos:
    __RESTART_X_RATIO, __RESTART_Y_RATIO = 1.30, 1.1

    def __init__(self, pos):
        self.__pos = pos

    @property
    def restart_pos(self):
        return self.__restart_x, self.__restart_y

    @property
    def height(self):
        return self.__pos.height

    @property
    def __restart_x(self):
        return self.__pos.width // self.__RESTART_X_RATIO

    @property
    def __restart_y(self):
        return self.__pos.height // self.__RESTART_Y_RATIO
