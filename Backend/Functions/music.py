from pygame import mixer
from pygame import time
from Frontend.Settings import SONG_VOLUME, HIT_SOUND_VOLUME, MISS_SOUND_VOLUME, SONG_FADE
from Backend.Timer import IntervalTimer, TargetTimer
from Backend.Map_Info.Map_Songs.songs_checker import SongChecker
import os


class Music:
    __ALL_MUSIC_DICT = {}
    __SOUND_INTERVAL = 90
    __SONG_FADE_MS = 100
    __ON_HIT_SOUNDS = True
    __SECOND_DELAY_BEFORE_REPEATING = -2

    def __init__(self, map_info=None):
        self.__music = None
        self.__song_volume = SONG_VOLUME
        self.__starting_ms = time.get_ticks()
        self.__mini_timer: IntervalTimer = IntervalTimer(self.__SOUND_INTERVAL)
        self.__timer: TargetTimer = TargetTimer()
        self.__map_info = map_info
        self.__song_checker = SongChecker()
        mixer.init()
        self.__init_all_songs()

    def __init_all_songs(self):
        for song in self.__song_checker.get_all_songs():
            self.__ALL_MUSIC_DICT[song] = mixer.Sound(os.path.join("Backend\Songs", f"{song}.mp3"))

    def set_music(self, song_name):
        self.__music = self.__ALL_MUSIC_DICT[song_name]

    def play_music(self):
        if self.__map_info is not None:
            self.set_music(song_name=self.__map_info.song_file_name)
        self.__start_music()
        self.__timer.restart()
        self.__timer.set_target_time(target_time=(seconds_length := self.__music.get_length()),
                                     end_song_delay=self.__SECOND_DELAY_BEFORE_REPEATING)
        return seconds_length

    def check_if_repeat(self):
        if self.__check_if_finished():
            self.play_music()

    def __check_if_finished(self):
        self.__timer.compute_if_finish_timer()
        if self.__timer.timer_finished:
            self.__timer.restart()
            return True
        return False

    @staticmethod
    def stop_music():
        mixer.Channel(2).stop()

    def restart_music(self):
        self.__song_volume = SONG_VOLUME
        self.__start_music()

    def reset_volume(self):
        self.__song_volume = SONG_VOLUME

    def __start_music(self):
        mixer.Channel(2).set_volume(self.__song_volume)
        mixer.Channel(2).stop()
        mixer.Channel(2).play(self.__music)

    def fade_music(self):
        ms_now = time.get_ticks()
        if ms_now - self.__starting_ms > self.__SONG_FADE_MS:
            self.__starting_ms = ms_now
            self.__song_volume -= SONG_FADE
            mixer.Channel(2).set_volume(self.__song_volume)

    @property
    def song_volume(self):
        return self.__song_volume

    @property
    def song_finished_fade(self) -> bool:
        if self.__song_volume <= 0.1:
            return True
        return False

    @staticmethod
    def pause_music():
        mixer.Channel(2).pause()

    @staticmethod
    def unpause_music():
        mixer.Channel(2).unpause()

    def play_hit_sound(self):
        if not self.__ON_HIT_SOUNDS:
            return
        if self.__mini_timer.time_interval_finished():
            sfx = mixer.Sound(os.path.join("Backend\Sfx", "Hit_Normal.wav"))
            mixer.Channel(3).set_volume(HIT_SOUND_VOLUME)
            mixer.Channel(3).play(sfx)

    @staticmethod
    def play_hit_sound_2():
        sfx = mixer.Sound(os.path.join("Backend\Sfx", "Hit_Finish.wav"))
        mixer.Channel(3).set_volume(HIT_SOUND_VOLUME)
        mixer.Channel(3).play(sfx)

    @staticmethod
    def play_miss_sound():
        sfx = mixer.Sound(os.path.join("Backend\Sfx", "Combo_Break.wav"))
        mixer.Channel(4).set_volume(MISS_SOUND_VOLUME)
        mixer.Channel(4).play(sfx)