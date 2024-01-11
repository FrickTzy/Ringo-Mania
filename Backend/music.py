from pygame import mixer
from pygame import time
from Frontend.settings import SONG_VOLUME, HIT_SOUND_VOLUME, MISS_SOUND_VOLUME, SONG_FADE
from Backend.timer import IntervalTimer
from Backend.Map_Info.Map_Songs.songs_checker import SongChecker
import os


class Music:
    __ALL_MUSIC_DICT = {}
    __SOUND_INTERVAL = 90
    __SONG_FADE_MS = 100
    __ON_HIT_SOUNDS = True

    def __init__(self, map_info=None):
        self.__music = None
        self.song_volume = SONG_VOLUME
        self.starting_ms = time.get_ticks()
        self.mini_timer: IntervalTimer = IntervalTimer(self.__SOUND_INTERVAL)
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
        return self.__music.get_length()

    def restart_music(self):
        self.song_volume = SONG_VOLUME
        self.__start_music()

    def __start_music(self):
        mixer.Channel(2).set_volume(self.song_volume)
        mixer.Channel(2).stop()
        mixer.Channel(2).play(self.__music)

    def fade_music(self):
        ms_now = time.get_ticks()
        if ms_now - self.starting_ms > self.__SONG_FADE_MS:
            self.starting_ms = ms_now
            self.song_volume -= SONG_FADE
            mixer.Channel(2).set_volume(self.song_volume)

    @property
    def song_finished_fade(self) -> bool:
        if self.song_volume <= 0.1:
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
        if self.mini_timer.time_interval_finished():
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
