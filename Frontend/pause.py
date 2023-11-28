from pygame import K_ESCAPE, time, Surface, SRCALPHA, SurfaceType, draw, K_TAB, mouse
from Stuff.Ringo_Mania.Backend.music import Music
from Stuff.Ringo_Mania.Backend.timer import Timer
from Stuff.Ringo_Mania.Frontend.font import Font
from Stuff.Ringo_Mania.Frontend.settings import WIDTH, HEIGHT, BLACK, WHITE


class Pause:
    __PAUSE_INTERVAL = 150
    __OPACITY_PERCENTAGE = 60
    __TEXT_POS_INTERVAL = 145
    __TEXT_POS_INTERVAL_RATIO = 6.21
    __PAUSE_Y = 115
    __PAUSE_Y_RATIO = 7.83
    __MAIN_FONT = "main_pause_font"
    __MINI_FONT = "pause_font"
    __PAUSE = "Pause"
    __CONTINUE = "Continue"
    __RESTART = "Restart"
    __QUIT = "Quit"

    def __init__(self, music: Music, mini_timer, font: Font):
        self.__starting_time: int = 0
        self.__paused = False
        self.__music = music
        self.__font = font
        self.mini_timer = mini_timer
        self.timer = Timer()
        self.__pause_surface = Surface((WIDTH, HEIGHT), SRCALPHA)
        self.__restarted = False

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
        self.__music.pause_music()
        self.pause_surface_setup(window_size)
        self.draw_to_pause_surface(window_size)
        self.show_text(window_size=window_size)
        window.blit(self.__pause_surface, (0, 0))
        mouse.set_visible(True)

    def update_text_coord(self, height: int):
        self.__TEXT_POS_INTERVAL = height // self.__TEXT_POS_INTERVAL_RATIO
        self.__PAUSE_Y = height // self.__PAUSE_Y_RATIO

    def show_text(self, window_size) -> None:
        text_coord = self.__font.get_text_center_coord(coord=window_size, font_type="main_pause_font",
                                                       text="Pause")
        self.update_text_coord(height=window_size[1])
        self.run_text(text_coord)

    def run_text(self, text_coord: tuple[int, int]):
        self.run_pause_text(text_coord)
        self.run_continue_text(text_coord)
        self.run_restart_text(text_coord)
        self.run_quit_text(text_coord)

    def run_pause_text(self, text_coord: tuple[int, int]) -> None:
        text_x, text_y = text_coord
        text = self.__font.main_pause_font.render(self.__PAUSE, True, WHITE)
        self.__pause_surface.blit(text, (text_x, self.__PAUSE_Y))

    def run_continue_text(self, text_coord: tuple[int, int]) -> None:
        text = self.__font.pause_font.render(self.__CONTINUE, True, WHITE)
        self.__pause_surface.blit(text, text_coord)
        self.check_buttons_for_clicks(starting_pos=text_coord,
                                      text_size=self.__font.pause_text_size(self.__MINI_FONT, self.__CONTINUE),
                                      command=self.unpause)

    def run_restart_text(self, text_coord: tuple[int, int]) -> None:
        text_x, text_y = text_coord
        text_coord = text_x, text_y + int(self.__TEXT_POS_INTERVAL)
        text = self.__font.pause_font.render(self.__RESTART, True, WHITE)
        self.__pause_surface.blit(text, text_coord)
        self.check_buttons_for_clicks(starting_pos=text_coord,
                                      text_size=self.__font.pause_text_size(self.__MINI_FONT, self.__RESTART),
                                      command=lambda: [self.set_restarted(), self.unpause()])

    def set_restarted(self):
        self.__restarted = True

    def run_quit_text(self, text_coord: tuple[int, int]) -> None:
        text_x, text_y = text_coord
        text_coord = text_x, text_y + int(self.__TEXT_POS_INTERVAL * 2)
        text = self.__font.pause_font.render(self.__QUIT, True, WHITE)
        self.__pause_surface.blit(text, text_coord)
        self.check_buttons_for_clicks(starting_pos=text_coord,
                                      text_size=self.__font.pause_text_size(self.__MINI_FONT, self.__QUIT),
                                      command=quit)

    def draw_to_pause_surface(self, window_size: tuple) -> None:
        r, g, b = BLACK
        width, height = window_size
        draw.rect(self.__pause_surface, (r, g, b, self.opacity), (0, 0, width, height))

    def unpause(self) -> None:
        self.__music.unpause_music()
        self.mini_timer.last_time += self.timer.get_time_spent()
        self.__paused = False
        mouse.set_visible(False)

    @staticmethod
    def get_ending_pos(starting_pos: tuple[int, int], text_size: tuple[int, int]) -> tuple[int, int]:
        starting_x, starting_y = starting_pos
        text_width, text_height = text_size
        return starting_x + text_width, starting_y + text_height

    def check_buttons_for_clicks(self, starting_pos: tuple[int, int], text_size: tuple[int, int], command):
        starting_x, starting_y = starting_pos
        ending_x, ending_y = self.get_ending_pos(starting_pos, text_size)
        x, y = mouse.get_pos()
        if (starting_x <= x <= ending_x and starting_y <= y <= ending_y) and mouse.get_pressed()[0]:
            command()

    @property
    def opacity(self) -> int:
        return self.percent_to_opacity(self.__OPACITY_PERCENTAGE)

    @staticmethod
    def percent_to_opacity(percent) -> int:
        return int(255 * (percent / 100))

    @property
    def time_spent_paused(self) -> int | float:
        return self.timer.get_time_spent()
