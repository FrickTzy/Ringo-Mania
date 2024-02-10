from Backend.timer import DelayTimer
from Frontend.Helper_Files.button_event_handler import ButtonEventHandler


class MapBarEventHandler:
    __CLICK_INTERVAL = 80

    def __init__(self, pos, index_manager, index, state, hover_manager):
        self.__timer = DelayTimer()
        self.__pos = pos
        self.__button_handler = ButtonEventHandler()
        self.__index_manager = index_manager
        self.__index = index
        self.__hover_manager = hover_manager
        self.__state = state

    def check_if_clicked(self, chosen: bool):
        if chosen:
            return self.__check_if_clicked_chosen()
        else:
            return self.__check_if_clicked_not_chosen()

    def __check_if_clicked_not_chosen(self):
        self.__timer.reset_timer()
        return self.__map_bar_click_checker(command=self.set_chosen)

    def __check_if_clicked_chosen(self):
        self.__timer.check_delay_ms(self.__CLICK_INTERVAL)
        if not self.__timer.timer_finished:
            return False
        return self.__map_bar_click_checker(command=self.__state.show_play_window)

    def __map_bar_click_checker(self, command) -> bool:
        clicked = self.__button_handler.check_buttons_for_clicks(starting_pos=self.__pos.record_starting_coord,
                                                                 size=self.__pos.current_size,
                                                                 command=command)
        if clicked:
            return True
        else:
            return False

    def check_if_hovered(self):
        if self.__button_handler.check_if_mouse_is_in_an_area(
                starting_pos=self.__pos.record_starting_coord,
                size=self.__pos.current_size):
            self.__set_hover()
            return True
        return False

    def __set_hover(self):
        self.__hover_manager.check_if_change_hover(hover_index=self.__index)

    def set_chosen(self):
        self.__index_manager.set_index(index=self.__index)
