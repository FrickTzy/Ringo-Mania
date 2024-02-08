from Frontend.Helper_Files.Transition.smooth_animation import SmoothAnimation
from Frontend.Helper_Files.Transition.target_manager import TargetManager
from .click_animation import ClickAnimation
from .hover_animation import HoverAnimation


class MapBarAnimation:
    __SPEED_PER_FRAME = 0.1
    __hovered = False

    def __init__(self, is_chosen: bool, map_bar_pos):
        self.__chosen = is_chosen
        self.__map_bar_pos = map_bar_pos
        self.__target_manager = TargetManager()
        self.__animation_manager = SmoothAnimation(target_manager=self.__target_manager,
                                                   speed_per_frame=self.__SPEED_PER_FRAME)
        self.__start_manager = AnimationStartManager()
        self.__hover_animation = HoverAnimation(map_bar_pos=map_bar_pos, smooth_animation=self.__animation_manager,
                                                start_manager=self.__start_manager,
                                                target_manager=self.__target_manager)
        self.__click_animation = ClickAnimation(map_bar_pos=map_bar_pos, smooth_animation=self.__animation_manager,
                                                start_manager=self.__start_manager,
                                                target_manager=self.__target_manager)

    def check_for_animation(self, is_chosen, is_hovered):
        if self.__correct_conditions(is_chosen=is_chosen, is_hovered=is_hovered):
            self.__animate_map_bar()

    def __correct_conditions(self, is_chosen, is_hovered):
        if not (self.__hover_animation.check_if_animate(is_chosen=is_chosen, is_hovered=is_hovered) or
                self.__click_animation.check_if_animate(is_chosen=is_chosen)):
            return False
        if self.__animation_manager.finished_animation:
            self.__start_manager.start_animation = False
            return False
        return True

    def __animate_map_bar(self):
        self.__map_bar_pos.set_current_width(width=self.__animation_manager.get_current_value())


class AnimationStartManager:
    start_animation = False
