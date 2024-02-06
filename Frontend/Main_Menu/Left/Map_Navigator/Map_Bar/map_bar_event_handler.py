from Backend.timer import DelayTimer
from Frontend.Helper_Files.button_event_handler import ButtonEventHandler


class MapBarEventHandler:
    __CLICK_INTERVAL = 80

    def __init__(self, pos, index_manager, index, state):
        self.__timer = DelayTimer()
        self.__pos = pos
        self.__button_handler = ButtonEventHandler()
        self.__index_manager = index_manager
        self.__index = index
        self.__state = state

    def check_if_clicked(self, chosen: bool):
        if chosen:
            return self.__check_if_clicked_chosen()
        else:
            return self.__check_if_clicked_not_chosen()

    def __check_if_clicked_not_chosen(self):
        self.__timer.reset_timer()
        clicked = self.__button_handler.check_buttons_for_clicks(starting_pos=self.__pos.record_starting_coord,
                                                                 size=self.__pos.record_size,
                                                                 command=lambda: self.set_chosen())
        if clicked:
            return True
        else:
            return False

    def __check_if_clicked_chosen(self):
        self.__timer.check_delay_ms(self.__CLICK_INTERVAL)
        if not self.__timer.timer_finished:
            return False
        clicked = self.__button_handler.check_buttons_for_clicks(starting_pos=self.__pos.record_starting_coord,
                                                                 size=self.__pos.chosen_map_bar_size,
                                                                 command=lambda: self.__state.show_play_window())
        if clicked:
            return True
        else:
            return False

    def check_if_hovered(self):
        if self.__button_handler.check_if_mouse_is_in_an_area(
                starting_pos=self.__pos.record_starting_coord,
                size=self.__pos.chosen_map_bar_size):
            return True
        return False

    def set_chosen(self):
        self.__index_manager.set_index(index=self.__index)
