from pygame import mixer
from pygame import time
from Stuff.Ringo_Mania.Frontend.settings import SONG_VOLUME, HIT_SOUND_VOLUME, MISS_SOUND_VOLUME, SONG_FADE, \
    SONG_FADE_MS
import os


class Music:
    def __init__(self):
        self.music: mixer.Sound
        self.song_volume = SONG_VOLUME
        self.starting_ms = time.get_ticks()

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
        if ms_now - self.starting_ms > SONG_FADE_MS:
            self.starting_ms = ms_now
            self.song_volume -= SONG_FADE
            mixer.Channel(2).set_volume(self.song_volume)

    @staticmethod
    def pause_music():
        mixer.Channel(2).pause()

    @staticmethod
    def unpause_music():
        mixer.Channel(2).unpause()

    @staticmethod
    def play_hit_sound():
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
