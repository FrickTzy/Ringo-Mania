import pygame
from Stuff.Ringo_Mania.Frontend.settings import FPS, BLACK, clock, \
    END_SONG_DELAY, KEY_BINDS
from Stuff.Ringo_Mania.Frontend.game_mode import GameModeWindow
from Stuff.Ringo_Mania.Frontend.main_rectangle import Rectangle
from Stuff.Ringo_Mania.Frontend.records import Record
from Stuff.Ringo_Mania.Frontend.font import Font
from Stuff.Ringo_Mania.Frontend.display import Display
from Stuff.Ringo_Mania.Frontend.combo import ComboCounter
from Stuff.Ringo_Mania.Frontend.pause import Pause
from Stuff.Ringo_Mania.Backend.timer import MiniTimer
from Stuff.Ringo_Mania.Frontend.show_acc import ShowAcc
from Stuff.Ringo_Mania.Frontend.map_status import MapStatus
from Stuff.Ringo_Mania.Frontend.stats import Stats


class ManiaPlayWindow(GameModeWindow):
    running = False
    imported = False

    def __init__(self, music, timer, map_manager, play_tracker, song="Bocchi"):
        super().__init__(display=Display(), font=Font(), music=music, play_tracker=play_tracker, timer=timer)
        self.record = Record(self.font, self.display)
        self.music.set_music(song)
        self.map_manager = map_manager(song)
        self.combo_counter = ComboCounter(self.font)
        self.circle_interval_timer = MiniTimer()
        self.show_acc = ShowAcc()
        self.stats = Stats(display=self.display)
        self.map_status = MapStatus(imported=self.imported)
        self.pause = Pause(music=self.music, mini_timer=self.circle_interval_timer, font=self.font)
        self.rectangle = Rectangle(maps=self.map_manager,
                                   display=self.display, combo_counter=self.combo_counter,
                                   mini_timer=self.circle_interval_timer, map_status=self.map_status,
                                   show_acc=self.show_acc)

    def run(self):
        self.background_setup()
        while self.running:
            self.timer.compute_time()
            self.update_frame()
            self.check_events()

            self.rectangle.run(current_time=self.timer.current_time, pause=self.pause.is_paused)
            self.show_stats_and_etc()
        pygame.quit()

    def restart(self):
        self.combo_counter.reset_all()
        self.show_acc.reset_acc()
        self.music.restart_music()
        self.timer.restart()
        self.map_status.failed = False
        self.rectangle.restart()

    def show_stats_and_etc(self):
        self.font.update_all_font(self.display.height)
        self.stats.show_all(play_info=self.combo_counter.get_play_info, life=self.combo_counter.life)
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

    def detect_key(self):
        key_pressed = pygame.key.get_pressed()
        if self.pause.check_pause(key_pressed):
            return
        for keys, index in KEY_BINDS.items():
            if key_pressed[eval(keys)]:
                self.rectangle.key_pressed(index=index)
                self.music.play_hit_sound()

    def check_events(self):
        self.detect_key()
        self.__check_map_if_failed()
        self.__check_if_missed()
        self.__check_window_if_quit()
        self.__check_map_if_finished()
        self.__check_window_if_paused()
        self.__check_window_if_restart()
        self.__check_window_if_resized()

    def __check_if_missed(self):
        if self.combo_counter.miss_sfx:
            self.music.play_miss_sound()
            self.combo_counter.miss_sfx = False

    def __check_map_if_failed(self):
        if self.combo_counter.life <= 0:
            print("he")
            self.map_status.failed = True
            self.music.fade_music()

    def __check_window_if_quit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def __check_map_if_finished(self):
        if self.timer.timer_finished or self.map_status.finished and not self.map_status.failed:
            self.map_status.finished = True
            self.play_tracker.update_plays(self.rectangle.combo_counter.get_stats())

    def __check_window_if_paused(self):
        if self.pause.is_paused:
            self.pause.show_pause(
                window_size=self.display.get_window_size,
                window=self.display.window)

    def __check_window_if_restart(self):
        if self.pause.restarted:
            self.restart()
            self.rectangle.restart()
            self.pause.restarted = False

    def __check_window_if_resized(self):
        if self.display.check_window_size():
            self.font.update_all_font(self.display.height)
            self.rectangle.update_rect()
