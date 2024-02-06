from Frontend.Helper_Files.Transition.smooth_animation import SmoothAnimation
from Frontend.Helper_Files.Transition.target_manager import TargetManager


class MapBarAnimation:
    __SPEED_PER_FRAME = 0.125
    __start_animation = False

    def __init__(self, is_chosen: bool, map_bar_pos):
        self.__chosen = is_chosen
        self.__map_bar_pos = map_bar_pos
        self.__target_manager = TargetManager()
        self.__animation_manager = SmoothAnimation(target_manager=self.__target_manager,
                                                   speed_per_frame=self.__SPEED_PER_FRAME)

    def check_for_animation(self, is_chosen):
        if not self.__correct_conditions(is_chosen=is_chosen):
            return
        self.__start_animation = True
        self.__chosen = is_chosen
        self.__animate_map_bar()

    def __animate_map_bar(self):
        self.__map_bar_pos.set_current_width(width=self.__animation_manager.get_current_value())

    def __correct_conditions(self, is_chosen):
        if not self.__start_animation:
            if self.__chosen == is_chosen:
                return False
            else:
                self.__animation_manager.reset()
                if is_chosen:
                    self.__target_manager.setup(current_value=self.__map_bar_pos.record_width,
                                                target_value=self.__map_bar_pos.chosen_record_width)
                else:
                    self.__target_manager.setup(current_value=self.__map_bar_pos.chosen_record_width,
                                                target_value=self.__map_bar_pos.record_width)
                return True
        if self.__animation_manager.finished_animation:
            self.__start_animation = False
            return False
        return True
