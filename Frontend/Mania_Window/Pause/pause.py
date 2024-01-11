from pygame import time, Surface, SRCALPHA, SurfaceType, draw, K_TAB, mouse
from Backend import Music
from Backend import Timer
from Frontend.Mania_Window.Misc.font import Font
from Frontend.settings import WIDTH, HEIGHT, BLACK, WHITE
from Frontend.Helper_Files import ButtonEventHandler


class Pause:
    __PAUSE_INTERVAL = 150

    def __init__(self, music: Music, mini_timer, font: Font, state):
        self.__starting_time: int = 0
        self.__paused = False
        self.__music = music
        self.__opacity = Opacity()
        self.__pos = PausePos()
        self.mini_timer = mini_timer
        self.timer = Timer()
        self.__state = state
        self.__pause_surface = Surface((WIDTH, HEIGHT), SRCALPHA)
        self.__restarted = False
        self.__text = PauseText(event_handler=ButtonEventHandler(), font=font, pos=self.__pos,
                                pause_surface=self.__pause_surface)

    def pause_surface_setup(self, window_size):
        width, height = window_size
        self.__pause_surface = Surface((width, height), SRCALPHA)

    def check_pause(self, key_pressed) -> bool:
        current_time = time.get_ticks()
        if key_pressed[K_TAB]:
            if current_time - self.__starting_time >= self.__PAUSE_INTERVAL:
                self.__starting_time = current_time
                if self.__paused:
                    self.unpause()
                    self.timer.end_time_ms()
                    self.__paused = False
                    return False
                else:
                    self.timer.reset_time()
                    self.timer.start_time_ms()
                    self.__paused = True
                    return True
        return False

    @property
    def is_paused(self) -> bool:
        return self.__paused

    @property
    def restarted(self) -> bool:
        return self.__restarted

    @restarted.setter
    def restarted(self, value):
        self.__restarted = value

    def show_pause(self, window_size: tuple[int, int], window: SurfaceType | Surface) -> None:
        mouse.set_visible(True)
        self.__music.pause_music()
        self.pause_surface_setup(window_size)
        self.draw_to_pause_surface(window_size)
        self.__text.show_text(window_size=window_size, pause_surface=self.__pause_surface,
                              commands={"unpause": self.unpause,
                                        "restart": lambda: [self.set_restarted(),
                                                            self.unpause()]})
        window.blit(self.__pause_surface, (0, 0))

    def set_restarted(self):
        self.__state.restart()

    def draw_to_pause_surface(self, window_size: tuple) -> None:
        r, g, b = BLACK
        width, height = window_size
        draw.rect(self.__pause_surface, (r, g, b, self.__opacity.opacity), (0, 0, width, height))

    def unpause(self) -> None:
        self.__music.unpause_music()
        self.mini_timer.last_time += self.timer.get_time_spent()
        self.__paused = False
        mouse.set_visible(False)

    @property
    def time_spent_paused(self) -> int | float:
        return self.timer.get_time_spent()


class PauseText:
    __MAIN_FONT = "main_pause_font"
    __MINI_FONT = "pause_font"
    __PAUSE = "Pause"
    __CONTINUE = "Continue"
    __RESTART = "Restart"
    __QUIT = "Quit"

    def __init__(self, event_handler, pause_surface, font, pos):
        self.__event_handler = event_handler
        self.__font = font
        self.__pause_surface = pause_surface
        self.__pos = pos

    def show_text(self, window_size, pause_surface, commands: dict) -> None:
        self.__update_surface(pause_surface=pause_surface)
        text_coord = self.__font.get_text_center_coord(coord=window_size, font_type="main_pause_font",
                                                       text="Pause")
        self.__pos.update_text_coord(height=window_size[1])
        unpause_command = commands["unpause"]
        restart_command = commands["restart"]
        self.__run_text(text_coord, unpause_command=unpause_command, restart_command=restart_command)

    def __update_surface(self, pause_surface):
        self.__pause_surface = pause_surface

    def __run_text(self, text_coord: tuple[int, int], unpause_command, restart_command):
        self.__run_pause_text(text_coord)
        self.__run_continue_text(text_coord, command=unpause_command)
        self.__run_restart_text(text_coord, command=restart_command)
        self.__run_quit_text(text_coord)

    def __run_pause_text(self, text_coord: tuple[int, int]) -> None:
        text_x, text_y = text_coord
        text = self.__font.main_pause_font.render(self.__PAUSE, True, WHITE)
        self.__pause_surface.blit(text, (text_x, self.__pos.PAUSE_Y))

    def __run_continue_text(self, text_coord: tuple[int, int], command) -> None:
        text = self.__font.pause_font.render(self.__CONTINUE, True, WHITE)
        self.__pause_surface.blit(text, text_coord)
        self.__event_handler.check_buttons_for_clicks(starting_pos=text_coord,
                                                      size=self.__font.pause_text_size(self.__MINI_FONT,
                                                                                       self.__CONTINUE),
                                                      command=command)

    def __run_restart_text(self, text_coord: tuple[int, int], command) -> None:
        text_x, text_y = text_coord
        text_coord = text_x, text_y + int(self.__pos.TEXT_POS_INTERVAL)
        text = self.__font.pause_font.render(self.__RESTART, True, WHITE)
        self.__pause_surface.blit(text, text_coord)
        self.__event_handler.check_buttons_for_clicks(starting_pos=text_coord,
                                                      size=self.__font.pause_text_size(self.__MINI_FONT,
                                                                                       self.__RESTART),
                                                      command=command)

    def __run_quit_text(self, text_coord: tuple[int, int]) -> None:
        text_x, text_y = text_coord
        text_coord = text_x, text_y + int(self.__pos.TEXT_POS_INTERVAL * 2)
        text = self.__font.pause_font.render(self.__QUIT, True, WHITE)
        self.__pause_surface.blit(text, text_coord)
        self.__event_handler.check_buttons_for_clicks(starting_pos=text_coord,
                                                      size=self.__font.pause_text_size(self.__MINI_FONT,
                                                                                       self.__QUIT),
                                                      command=quit)


class Opacity:
    __OPACITY_PERCENTAGE = 60

    @property
    def opacity(self) -> int:
        return self.percent_to_opacity(self.__OPACITY_PERCENTAGE)

    @staticmethod
    def percent_to_opacity(percent) -> int:
        return int(255 * (percent / 100))


class PausePos:
    TEXT_POS_INTERVAL = 145
    TEXT_POS_INTERVAL_RATIO = 6.21
    PAUSE_Y = 115
    PAUSE_Y_RATIO = 7.83

    def update_text_coord(self, height: int):
        self.TEXT_POS_INTERVAL = height // self.TEXT_POS_INTERVAL_RATIO
        self.PAUSE_Y = height // self.PAUSE_Y_RATIO
