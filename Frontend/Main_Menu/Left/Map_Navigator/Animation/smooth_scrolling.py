from Frontend.Helper_Files.Transition.smooth_animation import SmoothAnimation
from Frontend.Helper_Files.Transition.target_manager import TargetManager
from Frontend.Main_Menu.Left.Map_Navigator.Helper_Files.pos import MapNavigatorPos
from Backend.timer import ActivationTimer


class SmoothScroll:
    __SPEED_PER_FRAME = 0.15
    __scrolling = False
    __scroll_going_up = False
    __start_end_scroll = False

    def __init__(self, pos: MapNavigatorPos, view, list_manager):
        self.__target_manager = TargetManager()
        self.__animation_manager = SmoothAnimation(target_manager=self.__target_manager,
                                                   speed_per_frame=self.__SPEED_PER_FRAME)
        self.__list_manager = list_manager
        self.__scroll_speed_manager = ScrollSpeedManager()
        self.__unfiltered_animation = UnfilteredAnimation(view=view, list_manager=list_manager, pos=pos,
                                                          scroll_speed_manager=self.__scroll_speed_manager)
        self.__filtered_animation = FilteredAnimation(view=view, list_manager=list_manager, pos=pos,
                                                      scroll_speed_manager=self.__scroll_speed_manager)
        self.__activation_timer = ActivationTimer(interval=140)

    def check_if_scroll(self, scrolling, going_up):
        self.__scroll_condition(scrolling=scrolling, going_up=going_up)
        self.__change_scroll_speed()
        self.__check_if_end_scroll()
        if self.__scrolling:
            if self.__list_manager.using_filter:
                self.__filtered_animation.scroll(going_up=self.__scroll_going_up)
            else:
                self.__unfiltered_animation.scroll(going_up=self.__scroll_going_up)

    def __scroll_condition(self, scrolling, going_up):
        activation_stopped = self.__activation_timer.activation_stopped(activated=scrolling)
        if self.__scroll_going_up != going_up and going_up is not None:
            self.__scroll_going_up = going_up
        if self.__scrolling == scrolling:
            return
        if scrolling is False:
            if activation_stopped:
                self.__start_end_scroll = True
                self.__scrolling = scrolling
                self.__setup_out()
        else:
            if not self.__scrolling:
                self.__scroll_going_up = going_up
                self.__start_end_scroll = False
                self.__scrolling = scrolling
                self.__setup_in()

    def __check_if_end_scroll(self):
        if not self.__start_end_scroll:
            return
        if self.__list_manager.using_filter:
            self.__filtered_animation.scroll(going_up=self.__scroll_going_up)
        else:
            self.__unfiltered_animation.scroll(going_up=self.__scroll_going_up)
        if self.__animation_manager.finished_animation:
            self.__start_end_scroll = False

    def __change_scroll_speed(self):
        scroll_speed = self.__animation_manager.get_current_value()
        self.__scroll_speed_manager.set_current_scroll_speed(speed=scroll_speed)

    @staticmethod
    def __going_up(current_y, target_y):
        """
        if current_y is bigger than target_y, it means the scroll is going down.
        """
        if current_y >= target_y:
            return True
        else:
            return False

    def __setup_in(self):
        self.__animation_manager.reset()
        self.__target_manager.setup(current_value=0,
                                    target_value=self.__scroll_speed_manager.max_scroll_speed)

    def __setup_out(self):
        self.__animation_manager.reset()
        self.__target_manager.setup(current_value=self.__scroll_speed_manager.current_scroll_speed, target_value=0)


class FilteredAnimation:
    def __init__(self, view, list_manager, pos, scroll_speed_manager):
        self.__view = view
        self.__list_manager = list_manager
        self.__pos = pos
        self.__scroll_speed_manager = scroll_speed_manager

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

    def scroll(self, going_up: bool):
        if not len(self.__list_manager.filtered_map_bar_list) >= self.__view.MAX_BAR_VIEW:
            return
        if going_up:
            self.__scroll_up()
        else:
            self.__scroll_down()

    def __scroll_up(self):
        if self.__check_if_out_of_bound_filtered_scroll():
            return
        if self.__pos.filtered_starting_y > 300:
            return
        self.__pos.add_filtered_y(y=self.__scroll_speed_manager.current_scroll_speed)
        self.__update(going_up=False)

    def __scroll_down(self):
        if self.__check_if_out_of_bound_filtered_scroll():
            return
        if self.__view.filtered_top_view >= len(self.__list_manager.filtered_map_bar_list) - self.__view.MAX_BAR_SCROLL:
            return
        self.__pos.subtract_filtered_y(y=self.__scroll_speed_manager.current_scroll_speed)
        self.__update(going_up=True)

    def __check_if_out_of_bound_filtered_scroll(self):
        if not len(self.__list_manager.filtered_map_bar_list) >= self.__view.MAX_BAR_VIEW:
            return True

    def __update(self, going_up: bool):
        if going_up:
            self.__check_top_view()
        else:
            self.__check_bottom_view()


class UnfilteredAnimation:
    def __init__(self, pos: MapNavigatorPos, view, list_manager, scroll_speed_manager):
        self.__pos = pos
        self.__view = view
        self.__list_manager = list_manager
        self.__scroll_speed_manager = scroll_speed_manager

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

    def scroll(self, going_up: bool):
        if going_up:
            self.__scroll_up()
        else:
            self.__scroll_down()

    def __scroll_up(self):
        if self.__pos.record_starting_y >= 300:
            return
        self.__pos.add_y(y=self.__scroll_speed_manager.current_scroll_speed)
        self.__update(going_up=False)

    def __scroll_down(self):
        if self.__view.current_top_view >= len(self.__list_manager.map_bar_list) - self.__view.MAX_BAR_SCROLL:
            return
        self.__pos.subtract_y(y=self.__scroll_speed_manager.current_scroll_speed)
        self.__update(going_up=True)

    def __update(self, going_up: bool):
        if going_up:
            self.__check_top_view()
        else:
            self.__check_bottom_view()


class ScrollSpeedManager:
    __MAX_SCROLL_SPEED = 40
    __current_scroll_speed = 0

    @property
    def current_scroll_speed(self):
        return self.__current_scroll_speed

    def set_current_scroll_speed(self, speed):
        self.__current_scroll_speed = speed

    @property
    def max_scroll_speed(self):
        return self.__MAX_SCROLL_SPEED
