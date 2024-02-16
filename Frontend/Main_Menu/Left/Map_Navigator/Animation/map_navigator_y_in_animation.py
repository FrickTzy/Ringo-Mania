from Frontend.Helper_Files.Transition.Animation.smooth_animation import SmoothAnimation
from Frontend.Helper_Files.Transition.target_manager import TargetManager
from Frontend.Main_Menu.Left.Map_Navigator.Helper_Files.pos import MapNavigatorPos
from .animation_interface import AnimationInterface


class MapNavSmoothYInAnimation:
    __SPEED_PER_FRAME = 0.060
    __start_animation = False
    __current_animation_manager: AnimationInterface = None

    def __init__(self, pos: MapNavigatorPos, view, list_manager):
        self.__target_manager = TargetManager()
        self.__animation_manager = SmoothAnimation(target_manager=self.__target_manager,
                                                   speed_per_frame=self.__SPEED_PER_FRAME)
        self.__list_manager = list_manager
        self.__unfiltered_animation = UnfilteredAnimation(view=view, list_manager=list_manager, pos=pos)
        self.__filtered_animation = FilteredAnimation(view=view, list_manager=list_manager, pos=pos)

    def check_if_change_y(self):
        if self.__current_animation_manager is not self.__unfiltered_animation:
            self.__current_animation_manager = self.__unfiltered_animation
        self.__change_y()

    def check_if_change_filtered_y(self):
        if self.__current_animation_manager is not self.__filtered_animation:
            self.__current_animation_manager = self.__filtered_animation
        self.__change_y()

    def __change_y(self):
        if not self.__correct_conditions():
            return
        going_up = self.__going_up(current_y=self.__target_manager.current_value,
                                   target_y=self.__target_manager.target_value)
        self.__current_animation_manager.change_y(going_up=going_up,
                                                  current_y=self.__animation_manager.get_current_value())

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


class FilteredAnimation(AnimationInterface):
    def __init__(self, view, list_manager, pos):
        self.__view = view
        self.__list_manager = list_manager
        self.__pos = pos

    def __check_bottom_view(self):
        if self.__view.filtered_top_view == 0:
            return
        if self.__list_manager.filtered_map_bar_list[self.__view.filtered_top_view].change_top_index:
            self.__view.filtered_top_view -= 1

    def __check_top_view(self):
        if len(self.__list_manager.filtered_map_bar_list) - 1 <= self.__view.filtered_top_view:
            return
        if not self.__list_manager.filtered_map_bar_list[self.__view.filtered_top_view].is_viewed:
            self.__view.filtered_top_view += 1

    def change_y(self, going_up: bool, current_y):
        if not len(self.__list_manager.filtered_map_bar_list) >= self.__view.MAX_BAR_VIEW:
            return
        self.__pos.set_exact_filtered_y(y=current_y)
        self.__update(going_up=going_up)

    def __update(self, going_up: bool):
        if going_up:
            self.__check_top_view()
        else:
            self.__check_bottom_view()


class UnfilteredAnimation(AnimationInterface):
    def __init__(self, pos: MapNavigatorPos, view, list_manager):
        self.__pos = pos
        self.__target_manager = TargetManager()
        self.__view = view
        self.__list_manager = list_manager

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

    def change_y(self, going_up: bool, current_y):
        self.__pos.set_exact_y(y=current_y)
        self.__update(going_up=going_up)

    def __update(self, going_up: bool):
        if going_up:
            self.__check_top_view()
        else:
            self.__check_bottom_view()
