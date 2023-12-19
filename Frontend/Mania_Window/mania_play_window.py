import pygame
from Frontend.settings import FPS, BLACK, clock, \
    END_SONG_DELAY, KEY_BINDS
from Frontend.Mania_Window.Interfaces import GameModeWindow
from Frontend.Mania_Window.Rectangle import Rectangle
from Frontend.Mania_Window.Misc import Font, Display, MapStatus
from Frontend.Mania_Window.Stats import ComboCounter, ShowAcc, Stats, Record
from Frontend.Mania_Window.Pause import Pause
from Frontend.Mania_Window.End_Screen import EndScreen
from Backend import IntervalTimer, Music


class ManiaPlayWindow(GameModeWindow):
    running = False
    imported = False

    def __init__(self, music: Music, timer, map_manager, play_tracker, map_info):
        super().__init__(display=Display(), font=Font(), music=music, play_tracker=play_tracker, timer=timer,
                         play_state=PlayState())
        self.record = Record(self.font, self.display)
        self.music.set_music(map_info.song_name)
        self.map_manager = map_manager(map_info.song_name)
        self.combo_counter = ComboCounter(self.font)
        self.circle_interval_timer = IntervalTimer()
        self.show_acc = ShowAcc()
        self.stats = Stats(display=self.display)
        self.map_status = MapStatus(imported=self.imported)
        self.pause = Pause(music=self.music, mini_timer=self.circle_interval_timer, font=self.font, state=self.state)
        self.end_screen = EndScreen(window_size=self.display.get_window_size, state=self.state, map_info=map_info)
        self.rectangle = Rectangle(maps=self.map_manager,
                                   display=self.display, combo_counter=self.combo_counter,
                                   mini_timer=self.circle_interval_timer, map_status=self.map_status,
                                   show_acc=self.show_acc)
        self.event_handler = ManiaEventHandler(play_window=self)

    def run(self):
        self.background_setup()
        while self.running:
            self.timer.compute_time()
            self.update_frame()
            self.rectangle.run(current_time=self.timer.current_time, pause=self.pause.is_paused)
            self.show_stats_and_etc()
            self.event_handler.check_events()
        pygame.quit()

    def restart(self):
        self.combo_counter.reset_all()
        self.show_acc.reset_acc()
        self.music.restart_music()
        self.timer.restart()
        self.map_status.restart()
        self.rectangle.restart()
        self.end_screen.restart()

    def show_stats_and_etc(self):
        self.font.update_all_font(self.display.height)
        self.stats.show_all(play_info=self.combo_counter.get_play_info_text, life=self.combo_counter.life)
        self.record.show_record(current_rec=self.combo_counter.info)

    def background_setup(self):
        music_length = self.music.play_music()
        self.running = True
        self.timer.update_target_time(music_length, END_SONG_DELAY)
        self.record.init_record(self.play_tracker.check_plays())

    def update_frame(self):
        clock.tick(FPS)
        pygame.display.update()
        self.display.window.fill(BLACK)

    def show_end_screen(self):
        self.end_screen.show_end_screen(window=self.display.window, stats=self.combo_counter.get_stats,
                                        size=self.display.get_window_size)


class PlayState:
    def __init__(self):
        self.__restarted = False

    @property
    def restarted(self):
        return self.__restarted

    def restart(self):
        self.__restarted = True

    def un_restart(self):
        self.__restarted = False


class ManiaEventHandler:
    def __init__(self, play_window: ManiaPlayWindow):
        self.__play_window = play_window

    def check_events(self):
        self.__detect_key()
        self.__check_window_if_restart()
        self.__check_map_if_failed()
        self.__check_if_missed()
        self.__check_window_if_quit()
        self.__check_window_if_paused()
        self.__check_map_if_finished()
        self.__check_window_if_resized()

    def __detect_key(self):
        key_pressed = pygame.key.get_pressed()
        if self.__play_window.pause.check_pause(key_pressed):
            return
        for keys, index in KEY_BINDS.items():
            if key_pressed[eval(keys)]:
                self.__play_window.rectangle.key_pressed(index=index)
                self.__play_window.music.play_hit_sound()

    def __check_if_missed(self):
        if self.__play_window.combo_counter.miss_sfx:
            self.__play_window.music.play_miss_sound()
            self.__play_window.combo_counter.miss_sfx = False

    def __check_map_if_failed(self):
        if self.__play_window.combo_counter.life <= 0:
            self.__play_window.map_status.failed = True
            self.__play_window.music.fade_music()
            self.__play_window.show_end_screen()

    def __check_window_if_quit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__play_window.running = False

    def __check_map_if_finished(self):
        if (self.__play_window.timer.timer_finished or self.__play_window.map_status.finished) and \
                not (self.__play_window.map_status.failed and not self.__play_window.pause.is_paused):
            self.__play_window.map_status.finished = True
            self.__play_window.play_tracker.update_plays(self.__play_window.combo_counter.get_stats)
            self.__play_window.music.fade_music()
            self.__play_window.show_end_screen()

    def __check_window_if_paused(self):
        if self.__play_window.pause.is_paused:
            self.__play_window.pause.show_pause(
                window_size=self.__play_window.display.get_window_size,
                window=self.__play_window.display.window)

    def __check_window_if_restart(self):
        if self.__play_window.state.restarted:
            self.__play_window.restart()
            self.__play_window.rectangle.restart()
            self.__play_window.state.un_restart()

    def __check_window_if_resized(self):
        if self.__play_window.display.check_window_size():
            self.__play_window.font.update_all_font(self.__play_window.display.height)
            self.__play_window.rectangle.update_rect()
