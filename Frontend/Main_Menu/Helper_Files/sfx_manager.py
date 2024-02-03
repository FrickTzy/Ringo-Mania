from pygame import mixer
from os import path
from Frontend.Settings import SFX_VOLUME
from Backend.timer import IntervalTimer


class SFXManager:
    __SOUND_INTERVAL = 90
    __SFX_VOLUME = SFX_VOLUME
    __ON_SFX = True

    def __init__(self):
        self.__interval_timer = IntervalTimer(self.__SOUND_INTERVAL)
        self.__sound_manager = SoundManager()

    def play_menu_hit(self):
        self.__play_sfx(sound=self.__sound_manager.menu_hit_sound)

    def play_menu_back(self):
        self.__play_sfx(sound=self.__sound_manager.menu_back_sound)

    def play_menu_hover(self):
        self.__play_sfx(sound=self.__sound_manager.menu_hover_sound)

    def __play_sfx(self, sound):
        if not self.__ON_SFX:
            return
        if self.__interval_timer.time_interval_finished():
            mixer.Channel(3).set_volume(self.__SFX_VOLUME)
            mixer.Channel(3).play(sound)


class SoundManager:
    __PATH = "Backend\Sfx"
    __MENU_HIT_FILE = "Menu_Hit.wav"
    __MENU_BACK_FILE = "Menu_Back.wav"
    __MENU_HOVER_FILE = "Menu_Hover.wav"

    def __init__(self):
        self.__hit_sfx = mixer.Sound(path.join(self.__PATH, self.__MENU_HIT_FILE))
        self.__back_sfx = mixer.Sound(path.join(self.__PATH, self.__MENU_BACK_FILE))
        self.__hover_sfx = mixer.Sound(path.join(self.__PATH, self.__MENU_HOVER_FILE))

    @property
    def menu_hit_sound(self):
        return self.__hit_sfx

    @property
    def menu_back_sound(self):
        return self.__back_sfx

    @property
    def menu_hover_sound(self):
        return self.__hover_sfx
