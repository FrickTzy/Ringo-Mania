from Frontend.Helper_Files.Transition.smooth_animation import SmoothAnimation
from Frontend.Helper_Files.Transition.target_manager import TargetManager
from .pos import MapNavigatorPos


class MapNavSmoothYInAnimation:
    __SPEED_PER_FRAME = 0.060
    __start_animation = False

    def __init__(self, pos: MapNavigatorPos, view, list_manager):
        self.__pos = pos
        self.__target_manager = TargetManager()
        self.__view = view
        self.__list_manager = list_manager
        self.__animation_manager = SmoothAnimation(target_manager=self.__target_manager,
                                                   speed_per_frame=self.__SPEED_PER_FRAME)

    def check_if_change_y(self):
        if not self.__correct_conditions():
            return
        self.__pos.set_exact_y(y=self.__animation_manager.get_current_value())
        self.__update()

    def __update(self):
        if self.__going_up(current_y=self.__target_manager.current_value, target_y=self.__target_manager.target_value):
            self.__check_top_view()
        else:
            self.__check_bottom_view()

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

    @staticmethod
    def __going_up(current_y, target_y):
        """
        if current_y is bigger than target_y, it means the scroll is going down.
        """
        if current_y >= target_y:
            return True
        else:
            return False

    def __check_top_view(self):
        if len(self.__list_manager.map_bar_list) - 1 <= self.__view.current_top_view:
            return
        if not self.__list_manager.map_bar_list[self.__view.current_top_view].is_viewed:
            self.__view.current_top_view += 1

    def __check_bottom_view(self):
        if self.__view.current_top_view == 0:
            return
        if self.__list_manager.map_bar_list[self.__view.current_top_view].change_top_index:
            self.__view.current_top_view -= 1
