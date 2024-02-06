from pygame import key, K_RSHIFT, K_UP, K_DOWN
from Backend.timer import IntervalTimer
from Frontend.Helper_Files import ButtonEventHandler


class MapNavigatorEventHandler:
    __CLICK_INTERVAL = 80

    def __init__(self, list_manager, pos, view, notifier, sfx_manager):
        self.__interval_timer: IntervalTimer = IntervalTimer(interval=self.__CLICK_INTERVAL)
        self.__filtered_event_handler = FilteredEventHandler(view=view, pos=pos, list_manager=list_manager)
        self.__unfiltered_event_handler = UnfilteredEventHandler(list_manager=list_manager, pos=pos, view=view)
        self.__scroll_manager = ScrollManager(filtered_event_handler=self.__filtered_event_handler,
                                              list_manager=list_manager,
                                              unfiltered_event_handler=self.__unfiltered_event_handler)
        self.__mouse_event_handler = MouseEventHandler(button_event_handler=ButtonEventHandler(),
                                                       scroll_manager=self.__scroll_manager,
                                                       interval_timer=self.__interval_timer, pos=pos,
                                                       list_manager=list_manager,
                                                       filtered_event_handler=self.__filtered_event_handler,
                                                       unfiltered_event_handler=self.__unfiltered_event_handler,
                                                       notifier=notifier, sfx_manager=sfx_manager)
        self.__keyboard_event_handler = KeyboardEventHandler(scroll_manager=self.__scroll_manager,
                                                             list_manager=list_manager, sfx_manager=sfx_manager)

    def check_for_events(self, current_index):
        self.__mouse_event_handler.check_mouse_input_events(current_index=current_index)
        self.__keyboard_event_handler.check_keyboard_input_events(current_index=current_index)


class MouseEventHandler:
    def __init__(self, button_event_handler, scroll_manager, pos, interval_timer, list_manager, filtered_event_handler,
                 unfiltered_event_handler, notifier, sfx_manager):
        self.__button_event_handler = button_event_handler
        self.__scroll_manager: ScrollManager = scroll_manager
        self.__pos = pos
        self.__interval_timer = interval_timer
        self.__list_manager = list_manager
        self.__filtered_event_handler: FilteredEventHandler = filtered_event_handler
        self.__unfiltered_event_handler: UnfilteredEventHandler = unfiltered_event_handler
        self.__notifier = notifier
        self.__sfx_manager = sfx_manager

    def __check_if_scroll(self):
        if self.__notifier.scrolled:
            self.__scroll(event_occur=self.__notifier.event)

    def __scroll(self, event_occur):
        if event_occur.y > 0:
            self.__scroll_manager.go_up()
        else:
            self.__scroll_manager.go_down()

    def check_mouse_input_events(self, current_index):
        chosen_map_bar_hovered = self.__list_manager.map_bar_list[current_index].check_if_hovered()
        if not self.__check_mouse_pos_is_in_correct_position() and not chosen_map_bar_hovered:
            return
        self.__check_if_scroll()
        self.__check_if_clicked_record()

    def __check_mouse_pos_is_in_correct_position(self):
        if self.__button_event_handler.check_if_mouse_is_in_an_area(
                starting_pos=self.__pos.leaderboard_starting_pos,
                size=self.__pos.leaderboard_size):
            return True
        return False

    def __check_if_clicked_record(self):
        if not self.__interval_timer.time_interval_finished():
            return
        elif self.__list_manager.using_filter:
            if self.__filtered_event_handler.check_if_clicked_filtered_record():
                self.__sfx_manager.play_menu_hit()
        else:
            if self.__unfiltered_event_handler.check_if_clicked_unfiltered_record():
                self.__sfx_manager.play_menu_hit()


class KeyboardEventHandler:
    def __init__(self, scroll_manager, list_manager, sfx_manager):
        self.__scroll_manager = scroll_manager
        self.__list_manager = list_manager
        self.__sfx_manager = sfx_manager

    def __check_if_enter_key(self, key_pressed, map_bar):
        if key_pressed[K_RSHIFT]:
            self.__sfx_manager.play_menu_hit()
            map_bar.key_hit()

    def __check_if_enter_arrow_key(self, key_pressed):
        if key_pressed[K_UP]:
            self.__scroll_manager.go_up()
        elif key_pressed[K_DOWN]:
            self.__scroll_manager.go_down()

    def check_keyboard_input_events(self, current_index):
        key_pressed = key.get_pressed()
        self.__check_if_enter_key(key_pressed=key_pressed, map_bar=self.__list_manager.map_bar_list[current_index])
        self.__check_if_enter_arrow_key(key_pressed=key_pressed)


class ScrollManager:
    def __init__(self, list_manager, filtered_event_handler, unfiltered_event_handler):
        self.__list_manager = list_manager
        self.__filtered_event_handler: FilteredEventHandler = filtered_event_handler
        self.__unfiltered_event_handler: UnfilteredEventHandler = unfiltered_event_handler

    def go_up(self):
        if self.__list_manager.using_filter:
            self.__filtered_event_handler.go_up_filtered()
        else:

            self.__unfiltered_event_handler.go_up_unfiltered()

    def go_down(self):
        if self.__list_manager.using_filter:
            self.__filtered_event_handler.go_down_filtered()
        else:
            self.__unfiltered_event_handler.go_down_unfiltered()


class FilteredEventHandler:
    def __init__(self, view, list_manager, pos):
        self.__view = view
        self.__list_manager = list_manager
        self.__pos = pos

    def __check_filtered_bottom_view(self):
        if self.__view.filtered_top_view == 0:
            return
        if self.__list_manager.filtered_map_bar_list[self.__view.filtered_top_view].change_top_index:
            self.__view.filtered_top_view -= 1

    def __check_filtered_top_view(self):
        if len(self.__list_manager.filtered_map_bar_list) - 1 <= self.__view.filtered_top_view:
            return
        if not self.__list_manager.filtered_map_bar_list[self.__view.filtered_top_view].is_viewed:
            self.__view.filtered_top_view += 1

    def __check_if_out_of_bound_filtered_scroll(self):
        if not len(self.__list_manager.filtered_map_bar_list) >= self.__view.MAX_BAR_VIEW:
            return True

    def go_down_filtered(self):
        if self.__check_if_out_of_bound_filtered_scroll():
            return
        if self.__view.filtered_top_view >= len(self.__list_manager.filtered_map_bar_list) - self.__view.MAX_BAR_SCROLL:
            return
        self.__pos.change_filtered_starting_y(add=False)
        self.__check_filtered_top_view()

    def go_up_filtered(self):
        if self.__check_if_out_of_bound_filtered_scroll():
            return
        if self.__pos.filtered_starting_y > 300:
            return
        self.__pos.change_filtered_starting_y(add=True)
        self.__check_filtered_bottom_view()

    def check_if_clicked_filtered_record(self):
        map_bar_clicked = False
        for map_bar in self.__list_manager.filtered_map_bar_list:
            current_map_bar_clicked = map_bar.check_if_clicked()
            if not map_bar_clicked:
                map_bar_clicked = current_map_bar_clicked
        return map_bar_clicked


class UnfilteredEventHandler:
    def __init__(self, view, list_manager, pos):
        self.__view = view
        self.__list_manager = list_manager
        self.__pos = pos

    def go_down_unfiltered(self):
        if self.__check_if_out_of_bound_unfiltered_scroll():
            return
        if self.__view.current_top_view >= len(self.__list_manager.map_bar_list) - self.__view.MAX_BAR_SCROLL:
            return
        self.__pos.change_starting_y(add=False)
        self.__check_unfiltered_top_view()

    def __check_if_out_of_bound_unfiltered_scroll(self):
        if not len(self.__list_manager.map_bar_list) >= self.__view.MAX_BAR_VIEW:
            return True

    def __check_unfiltered_top_view(self):
        if len(self.__list_manager.map_bar_list) - 1 <= self.__view.current_top_view:
            return
        if not self.__list_manager.map_bar_list[self.__view.current_top_view].is_viewed:
            self.__view.current_top_view += 1

    def __check_unfiltered_bottom_view(self):
        if self.__view.current_top_view == 0:
            return
        if self.__list_manager.map_bar_list[self.__view.current_top_view].change_top_index:
            self.__view.current_top_view -= 1

    def go_up_unfiltered(self):
        if self.__check_if_out_of_bound_unfiltered_scroll():
            return
        if self.__pos.record_starting_y >= 300:
            return
        self.__pos.change_starting_y(add=True)
        self.__check_unfiltered_bottom_view()

    def check_if_clicked_unfiltered_record(self):
        map_bar_clicked = False
        for map_bar in self.__list_manager.map_bar_list:
            current_map_bar_clicked = map_bar.check_if_clicked()
            if not map_bar_clicked:
                map_bar_clicked = current_map_bar_clicked
        return map_bar_clicked
