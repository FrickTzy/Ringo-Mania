import pygame
from Stuff.Ringo_Mania.Frontend.settings import FPS, COMBO_X, SCORE_Y, BLACK, clock, \
    PURPLE, END_SONG_DELAY, MID_COMBO_X, MID_COMBO_Y, RECT_COMBO_DISPLAY, \
    RECORD_X, KEY_BINDS
from Stuff.Ringo_Mania.Frontend.main_rectangle import Rectangle
from Stuff.Ringo_Mania.Frontend.records import Record
from Stuff.Ringo_Mania.Frontend.font import Font
from Stuff.Ringo_Mania.Frontend.display import Display
from Stuff.Ringo_Mania.Frontend.combo import ComboCounter
from Stuff.Ringo_Mania.Frontend.pause import Pause
from Stuff.Ringo_Mania.Backend.timer import MiniTimer
from Stuff.Ringo_Mania.Frontend.show_acc import ShowAcc
from Stuff.Ringo_Mania.Frontend.map_status import MapStatus


class PlayWindow:
    running = False
    imported = False

    def __init__(self, music, timer, map_manager, play_tracker, song="Bocchi"):
        self.display: Display = Display()
        self.font = Font()
        self.record = Record(self.font)
        self.music = music
        self.play_tracker = play_tracker
        self.music.set_music(song)
        self.timer = timer
        self.map_manager = map_manager(song)
        self.combo_counter = ComboCounter(self.font)
        self.circle_interval_timer = MiniTimer()
        self.show_acc = ShowAcc()
        self.map_status = MapStatus(imported=self.imported)
        self.pause = Pause(music=self.music, mini_timer=self.circle_interval_timer, font=self.font)
        self.rectangle = Rectangle(window=self.display.window, music=self.music, maps=self.map_manager,
                                   display=self.display, combo_counter=self.combo_counter, pause=self.pause,
                                   mini_timer=self.circle_interval_timer, map_status=self.map_status,
                                   show_acc=self.show_acc)

    def run(self):
        self.background_setup()
        while self.running:
            self.timer.compute_time()
            self.update_frame()
            self.rectangle.run(current_time=self.timer.current_time)
            self.show_record()
            self.show_combo_and_life()
            self.check_events()
        pygame.quit()

    def restart(self):
        self.combo_counter.reset_all()
        self.show_acc.reset_acc()
        self.music.restart_music()
        self.timer.restart()
        self.map_status.failed = False
        self.rectangle.restart()

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

    def check_events(self):
        self.__check_map_if_failed()
        self.__check_window_if_quit()
        self.__check_map_if_finished()
        self.__check_window_if_paused()
        self.__check_window_if_restart()
        self.__check_window_if_resized()

    def __check_map_if_failed(self):
        if self.combo_counter.life == 0:
            self.map_status.failed = True

    def __check_window_if_quit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def __check_map_if_finished(self):
        if self.timer.timer_finished or self.map_status.finished and not self.map_status.failed:
            self.rectangle.map_finished = True
            self.play_tracker.update_plays(self.rectangle.combo_counter.get_stats())

    def __check_window_if_paused(self):
        if self.pause.is_paused:
            self.pause.show_pause(
                window_size=self.display.get_window_size,
                window=self.display.window)

    def __check_window_if_restart(self):
        if self.rectangle.pause.restarted:
            self.rectangle.restart()
            self.rectangle.pause.restarted = False

    def __check_window_if_resized(self):
        if self.display.check_window_size():
            self.rectangle.update_rect()
            self.combo_counter.change_life_bar_coord(self.display.life_bar_coord_x)
