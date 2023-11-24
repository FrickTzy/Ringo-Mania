from pygame import K_ESCAPE, time, Surface, SRCALPHA, SurfaceType, draw, K_TAB
from Stuff.Ringo_Mania.Backend.music import Music
from Stuff.Ringo_Mania.Backend.timer import Timer
from Stuff.Ringo_Mania.Frontend.font import Font
from Stuff.Ringo_Mania.Frontend.settings import WIDTH, HEIGHT, BLACK, WHITE


class Pause:
    __PAUSE_INTERVAL = 200
    __OPACITY_PERCENTAGE = 50

    def __init__(self, music: Music, mini_timer, font: Font):
        self.__starting_time: int = 0
        self.__paused = False
        self.__music = music
        self.__font = font
        self.mini_timer = mini_timer
        self.timer = Timer()
        self.__pause_surface = Surface((WIDTH, HEIGHT), SRCALPHA)

    def pause_surface_setup(self, window_size):
        width, height = window_size
        self.__pause_surface = Surface((width, height), SRCALPHA)

    def check_pause(self, key_pressed) -> None:
        current_time = time.get_ticks()
        if key_pressed[K_TAB]:
            if current_time - self.__starting_time >= self.__PAUSE_INTERVAL:
                # print("escaped")
                self.__starting_time = current_time
                if self.__paused:
                    self.unpause()
                    self.timer.end_time_ms()
                    self.__paused = False
                else:
                    self.timer.reset_time()
                    self.timer.start_time_ms()
                    self.__paused = True

    @property
    def is_paused(self) -> bool:
        return self.__paused

    def show_pause(self, window_size, window: SurfaceType | Surface, text_pos: tuple[int, int]) -> None:
        self.__music.pause_music()
        self.pause_surface_setup(window_size)
        self.draw_to_pause_surface(window_size)
        self.show_text(text_pos)
        window.blit(self.__pause_surface, (0, 0))

    def show_text(self, text_pos):
        text_x, text_y = text_pos
        text = self.__font.main_font.render(f"Game Paused", True, WHITE)
        self.__pause_surface.blit(text, (text_x, text_y))

    def draw_to_pause_surface(self, window_size: tuple):
        r, g, b = BLACK
        width, height = window_size
        draw.rect(self.__pause_surface, (r, g, b, self.opacity), (0, 0, width, height))

    def unpause(self):
        self.__music.unpause_music()
        self.mini_timer.last_time += self.timer.get_time_spent()

    @property
    def opacity(self) -> int:
        return self.percent_to_opacity(self.__OPACITY_PERCENTAGE)

    @staticmethod
    def percent_to_opacity(percent) -> int:
        return int(255 * (percent / 100))

    @property
    def time_spent_paused(self) -> int | float:
        return self.timer.get_time_spent()
