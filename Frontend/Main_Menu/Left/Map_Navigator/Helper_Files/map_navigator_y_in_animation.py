from Frontend.Helper_Files.Transition.smooth_animation import SmoothAnimation
from Frontend.Helper_Files.Transition.target_manager import TargetManager
from .pos import MapNavigatorPos


class MapNavSmoothYInAnimation:
    __SPEED_PER_FRAME = 0.060
    __start_animation = False

    def __init__(self, pos: MapNavigatorPos):
        self.__pos = pos
        self.__target_manager = TargetManager()
        self.__animation_manager = SmoothAnimation(target_manager=self.__target_manager,
                                                   speed_per_frame=self.__SPEED_PER_FRAME)

    def check_if_change_y(self):
        if not self.__correct_conditions():
            return
        self.__pos.set_exact_y(y=self.__animation_manager.get_current_value())

    def __correct_conditions(self):
        if not self.__start_animation:
            return False
        if self.__animation_manager.finished_animation:
            self.__start_animation = False
            return False
        return True

    def setup(self, current_y, target_y):
        self.__animation_manager.reset()
        self.__target_manager.setup(current_value=current_y, target_value=target_y)
        self.__start_animation = True
