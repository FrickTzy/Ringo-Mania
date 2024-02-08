class HoverAnimation:
    __hovered = False

    def __init__(self, map_bar_pos, target_manager, smooth_animation, start_manager):
        self.__map_bar_pos = map_bar_pos
        self.__target_manager = target_manager
        self.__animation_manager = smooth_animation
        self.__start_manager = start_manager

    def check_if_animate(self, is_chosen, is_hovered):
        if not self.__hovered == is_hovered:
            self.__setup_animation(is_chosen=is_chosen, is_hovered=is_hovered)
        if self.__start_manager.start_animation:
            return True
        return False

    def __setup_animation(self, is_hovered, is_chosen):
        self.__animation_manager.reset()
        if is_hovered:
            self.__target_manager.setup(current_value=self.__map_bar_pos.current_map_bar_width,
                                        target_value=self.__map_bar_pos.hover_width)
        else:
            if is_chosen:
                self.__target_manager.setup(current_value=self.__map_bar_pos.current_map_bar_width,
                                            target_value=self.__map_bar_pos.chosen_record_width)
            else:
                self.__target_manager.setup(current_value=self.__map_bar_pos.current_map_bar_width,
                                            target_value=self.__map_bar_pos.record_width)
        self.__hovered = is_hovered
        self.__start_manager.start_animation = True
