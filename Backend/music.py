from pygame import mixer
from pygame import time
from Frontend.settings import SONG_VOLUME, HIT_SOUND_VOLUME, MISS_SOUND_VOLUME, SONG_FADE
from Backend.timer import IntervalTimer
import os


class Music:
    __SOUND_INTERVAL = 90
    __SONG_FADE_MS = 100
    __ON_HIT_SOUNDS = True

    def __init__(self):
        self.music: mixer.Sound
        self.song_volume = SONG_VOLUME
        self.starting_ms = time.get_ticks()
        self.mini_timer: IntervalTimer = IntervalTimer(self.__SOUND_INTERVAL)

    def set_music(self, song_name):
        mixer.init()
        self.music = mixer.Sound(os.path.join("Backend\Songs", f"{song_name}.mp3"))

    def play_music(self):
        mixer.Channel(2).set_volume(self.song_volume)
        mixer.Channel(2).play(self.music)
        return self.music.get_length()

    def restart_music(self):
        self.song_volume = SONG_VOLUME
        mixer.Channel(2).stop()
        self.play_music()

    def fade_music(self):
        ms_now = time.get_ticks()
        if ms_now - self.starting_ms > self.__SONG_FADE_MS:
            self.starting_ms = ms_now
            self.song_volume -= SONG_FADE
            print(self.song_volume)
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
