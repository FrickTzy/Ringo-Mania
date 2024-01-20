import pygame
from Frontend.Settings import END_SONG_DELAY, KEY_BINDS
from Frontend.Mania_Window.Interfaces import GameModeWindow
from Frontend.Mania_Window.Rectangle import Rectangle
from Frontend.Mania_Window.Misc import Font, MapStatus
from Frontend.Mania_Window.Stats import ComboCounter, ShowAcc, Stats, Record
from Frontend.Mania_Window.Pause import Pause
from Frontend.Mania_Window.End_Screen import EndScreen
from Frontend.Helper_Files.Interfaces import State, WindowEventHandler
from Backend import IntervalTimer, Music


class ManiaPlayWindow(GameModeWindow):
    imported = False
    __setup_finished = False

    def __init__(self, music: Music, timer, map_manager, play_tracker, map_info, display, window_manager):
        super().__init__(display=display, font=Font(), music=music, play_tracker=play_tracker, timer=timer,
                         play_state=PlayState())
        self.record = Record(font=self.font, display=self.display)
        self.map_manager = map_manager(map_info=map_info)
        self.combo_counter = ComboCounter(font=self.font)
        self.circle_interval_timer = IntervalTimer()
        self.show_acc = ShowAcc()
        self.map_status = MapStatus(imported=self.imported)
        self.pause = Pause(music=self.music, mini_timer=self.circle_interval_timer, font=self.font, state=self.state)
        self.end_screen = EndScreen(window_size=self.display.get_window_size, state=self.state, map_info=map_info)
        self.rectangle = Rectangle(maps=self.map_manager,
                                   display=self.display, combo_counter=self.combo_counter,
                                   mini_timer=self.circle_interval_timer, map_status=self.map_status,
                                   show_acc=self.show_acc)
        self.stats = Stats(display=self.display, rectangle_pos=self.rectangle.pos_class)
        self.event_handler = ManiaEventHandler(play_window=self, window_manager=window_manager)

    def run(self):
        self.background_setup()
        self.timer.compute_if_finish_timer()
        self.rectangle.run(current_time=self.timer.current_time, pause=self.pause.is_paused)
        self.show_stats_and_etc()
        self.event_handler.check_events()

    def restart(self):
        self.combo_counter.reset_all()
        self.show_acc.reset_acc()
        self.music.restart_music()
        self.timer.restart()
        self.map_status.restart()
        self.rectangle.restart()
        self.end_screen.restart()
        self.state.un_restart()
        self.record.init_record(self.play_tracker.check_plays())
        self.state.reset_all()

    def show_stats_and_etc(self):
        self.font.update_all_font(self.display.height)
        self.stats.show_all(play_info=self.combo_counter.get_play_info_text, life=self.combo_counter.life)
        self.record.show_record(current_rec=self.combo_counter.info)

    def background_setup(self):
        if self.__setup_finished:
            return
        music_length = self.music.play_music()
        self.timer.update_target_time(music_length, END_SONG_DELAY)
        self.record.init_record(self.play_tracker.check_plays())
        self.display.show_cursor(show=False)
        self.__setup_finished = True

    def show_end_screen(self):
        self.end_screen.show_end_screen(window=self.display.window, stats=self.combo_counter.get_stats,
                                        size=self.display.get_window_size, date_time=self.combo_counter.date_time,
                                        grade=self.combo_counter.get_grade)


class PlayState(State):
    def __init__(self):
        self.__restarted = False
        self.__leave_mania = False

    @property
    def leave_mania(self):
        return self.__leave_mania

    def enter_playing_window(self):
        self.__leave_mania = False

    def leave_score_screen(self):
        self.__leave_mania = True

    @property
    def restarted(self):
        return self.__restarted

    def restart(self):
        self.__restarted = True

    def un_restart(self):
        self.__restarted = False

    def reset_all(self):
        self.un_restart()
        self.enter_playing_window()


class ManiaEventHandler(WindowEventHandler):
    def __init__(self, play_window: ManiaPlayWindow, window_manager):
        self.__play_window = play_window
        self.__window_manager = window_manager

    def check_events(self):
        self.__detect_key()
        self.__check_window_if_restart()
        self.__check_map_if_failed()
        self.__check_if_missed()
        self.check_window_if_quit()
        self.__check_window_if_paused()
        self.__check_map_if_finished()
        self.__check_window_if_resized()
        self.__check_if_leave_play_window()

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

    def check_window_if_quit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__window_manager.quit()

    def __check_if_leave_play_window(self):
        if not self.__play_window.state.leave_mania:
            return
        self.__window_manager.show_main_menu()

    def __check_map_if_finished(self):
        if (self.__play_window.timer.timer_finished or self.__play_window.map_status.finished) and \
                not (self.__play_window.map_status.failed and not self.__play_window.pause.is_paused):
            self.__play_window.map_status.finished = True
            self.__play_window.play_tracker.update_plays(self.__play_window.combo_counter.get_stats)
            self.__play_window.music.fade_music()
            self.__play_window.show_end_screen()
            self.__play_window.map_manager.overwrite_map()

    def __check_window_if_paused(self):
        if self.__play_window.pause.is_paused:
            self.__play_window.pause.show_pause(
                window_size=self.__play_window.display.get_window_size,
                window=self.__play_window.display.window)

    def __check_window_if_restart(self):
        if self.__play_window.state.restarted:
            self.__play_window.restart()

    def __check_window_if_resized(self):
        if self.__play_window.display.check_window_size():
            self.__play_window.font.update_all_font(self.__play_window.display.height)
            self.__play_window.rectangle.update_rect()
