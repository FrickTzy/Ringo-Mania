from .map_navigator_y_in_animation import MapNavSmoothYInAnimation


class AnimationManager:
    def __init__(self, pos, view, list_manager):
        self.__y_animation = MapNavSmoothYInAnimation(view=view, list_manager=list_manager, pos=pos)
        self.__list_manager = list_manager
        self.__pos = pos

    def setup(self, current_index):
        if self.__list_manager.using_filter:
            top_view = self.__list_manager.filtered_map_bar_list.index(
                self.__list_manager.map_bar_list[current_index]) - 2
            current_y = self.__pos.filtered_starting_y
        else:
            top_view = current_index - 2
            current_y = self.__pos.record_starting_y
        target_y = self.__pos.get_target_y(index=top_view)
        self.__y_animation.setup(current_y=current_y, target_y=target_y)

    def check_for_animation(self):
        if self.__list_manager.using_filter:
            self.__y_animation.check_if_change_filtered_y()
        else:
            self.__y_animation.check_if_change_y()
