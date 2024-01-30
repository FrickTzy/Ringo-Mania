from .animation import Animation
from .target_manager import TargetManager


class SmoothAnimation:
    __reset_animation = False
    __finished_animation = False

    def __init__(self, target_manager: TargetManager, speed_per_frame):
        self.__animation = Animation(ms_interval_per_iteration=speed_per_frame)
        self.__target_manager = target_manager

    def reset(self):
        self.__reset_animation = False
        self.__finished_animation = False
        self.__animation.reset()

    def __smooth_out_animation(self):
        if not self.__reset_animation:
            self.__animation.reset()
        self.__reset_animation = True

    def get_current_value(self):
        value = self.__target_manager.current_value + self.__get_add_value
        if self.__target_manager.check_if_equal_target_value(value=value):
            self.__finished_animation = True
        return value

    @property
    def __get_add_value(self):
        return self.__target_manager.target_value_range * self.__animation.get_current_percentage()

    @property
    def finished_animation(self):
        return self.__finished_animation
