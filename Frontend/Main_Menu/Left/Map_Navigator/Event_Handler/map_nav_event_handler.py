from pygame import key, K_RETURN, K_UP, K_DOWN, K_BACKSPACE
from Backend.timer import IntervalTimer, ActivationTimer
from Frontend.Helper_Files import ButtonEventHandler


class MapNavigatorEventHandler:
    __CLICK_INTERVAL = 80

    def __init__(self, list_manager, pos, notifier, sfx_manager, hover_manager, scroll_manager, search_tracker):
        self.__interval_timer: IntervalTimer = IntervalTimer(interval=self.__CLICK_INTERVAL)
        self.__filtered_event_handler = FilteredEventHandler(list_manager=list_manager)
        self.__unfiltered_event_handler = UnfilteredEventHandler(list_manager=list_manager)
        self.__mouse_event_handler = MouseEventHandler(button_event_handler=ButtonEventHandler(),
                                                       scroll_manager=scroll_manager,
                                                       interval_timer=self.__interval_timer, pos=pos,
                                                       list_manager=list_manager,
                                                       filtered_event_handler=self.__filtered_event_handler,
                                                       unfiltered_event_handler=self.__unfiltered_event_handler,
                                                       notifier=notifier, sfx_manager=sfx_manager,
                                                       hover_manager=hover_manager)
        self.__keyboard_event_handler = KeyboardEventHandler(scroll_manager=scroll_manager,
                                                             list_manager=list_manager, sfx_manager=sfx_manager,
                                                             search_tracker=search_tracker)

    def check_for_events(self, current_index):
        self.__mouse_event_handler.check_mouse_input_events(current_index=current_index)
        self.__keyboard_event_handler.check_keyboard_input_events(current_index=current_index)


class MouseEventHandler:
    def __init__(self, button_event_handler, pos, interval_timer, list_manager, filtered_event_handler,
                 unfiltered_event_handler, notifier, sfx_manager, hover_manager, scroll_manager):
        self.__button_event_handler = button_event_handler
        self.__scroll_manager = scroll_manager
        self.__pos = pos
        self.__interval_timer = interval_timer
        self.__list_manager = list_manager
        self.__filtered_event_handler: FilteredEventHandler = filtered_event_handler
        self.__unfiltered_event_handler: UnfilteredEventHandler = unfiltered_event_handler
        self.__notifier = notifier
        self.__sfx_manager = sfx_manager
        self.__hover_manager = hover_manager

    def __check_if_scroll(self):
        """This is some risky code, since I check scrolling twice"""
        scrolling = self.__notifier.scrolled
        going_up = self.__going_up(event_occur=self.__notifier.event) if scrolling else None
        if scrolling:
            self.__scroll_manager.check_if_scroll(scrolling=scrolling, going_up=going_up)

    @staticmethod
    def __going_up(event_occur):
        if event_occur.y > 0:
            return True
        else:
            return False

    def check_mouse_input_events(self, current_index):
        chosen_map_bar_hovered = self.__list_manager.map_bar_list[current_index].check_if_hovered()
        if not self.__check_mouse_pos_is_in_correct_position() and not chosen_map_bar_hovered:
            return
        self.__check_if_scroll()
        self.__check_if_play_hover_sfx()
        self.__check_if_clicked_record()

    def __check_mouse_pos_is_in_correct_position(self):
        if self.__button_event_handler.check_if_mouse_is_in_an_area(
                starting_pos=self.__pos.leaderboard_starting_pos,
                size=self.__pos.scrollable_area):
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

    def __check_if_play_hover_sfx(self):
        if self.__hover_manager.changed_hover:
            self.__sfx_manager.play_menu_hover()


class KeyboardEventHandler:
    def __init__(self, scroll_manager, list_manager, sfx_manager, search_tracker):
        self.__scroll_manager = scroll_manager
        self.__list_manager = list_manager
        self.__sfx_manager = sfx_manager
        self.__search_backspace_tracker = SearchBackspaceTracker(search_tracker=search_tracker)

    def __check_if_enter_key(self, key_pressed, map_bar):
        if key_pressed[K_RETURN]:
            self.__sfx_manager.play_menu_hit()
            map_bar.key_hit()

    def __check_if_scroll(self, key_pressed):
        """This is some risky code, since I check scrolling twice"""
        scrolling, going_up = self.__check_if_enter_arrow_key(key_pressed=key_pressed)
        self.__scroll_manager.check_if_scroll(scrolling=scrolling, going_up=going_up)

    @staticmethod
    def __check_if_enter_arrow_key(key_pressed):
        scrolling = False
        going_up = None
        if key_pressed[K_UP]:
            scrolling = True
            going_up = True
        elif key_pressed[K_DOWN]:
            scrolling = True
            going_up = False
        return scrolling, going_up

    def check_keyboard_input_events(self, current_index):
        key_pressed = key.get_pressed()
        self.__search_backspace_tracker.check_if_hold_backspace(key_pressed=key_pressed)
        self.__check_if_enter_key(key_pressed=key_pressed, map_bar=self.__list_manager.map_bar_list[current_index])
        self.__check_if_scroll(key_pressed=key_pressed)


class SearchBackspaceTracker:
    __BACKSPACE_HOLD_INTERVAL = 200
    __REMOVE_CHARACTER_INTERVAL = 50
    __hold_backspace = False

    def __init__(self, search_tracker):
        self.__search_tracker = search_tracker
        self.__activation_timer = ActivationTimer(interval=self.__BACKSPACE_HOLD_INTERVAL)
        self.__remover_timer = ActivationTimer(interval=self.__REMOVE_CHARACTER_INTERVAL)

    def check_if_hold_backspace(self, key_pressed):
        pressed_backspace = key_pressed[K_BACKSPACE]
        finished_interval = self.__remover_timer.activation_started(activated=pressed_backspace)
        self.__check_if_started_holding_backspace(pressed_backspace=pressed_backspace)
        if not pressed_backspace:
            self.__hold_backspace = False
            return
        if not self.__hold_backspace:
            return
        if not finished_interval:
            return
        self.__search_tracker.remove_a_letter()

    def __check_if_started_holding_backspace(self, pressed_backspace: bool):
        activation_complete = self.__activation_timer.activation_started(activated=pressed_backspace)
        if activation_complete:
            self.__hold_backspace = True


class FilteredEventHandler:
    def __init__(self, list_manager):
        self.__list_manager = list_manager

    def check_if_clicked_filtered_record(self):
        map_bar_clicked = False
        for map_bar in self.__list_manager.filtered_map_bar_list:
            if not map_bar.is_viewed:
                continue
            current_map_bar_clicked = map_bar.check_if_clicked()
            if not map_bar_clicked:
                map_bar_clicked = current_map_bar_clicked
        return map_bar_clicked


class UnfilteredEventHandler:
    def __init__(self, list_manager):
        self.__list_manager = list_manager

    def check_if_clicked_unfiltered_record(self):
        map_bar_clicked = False
        for map_bar in self.__list_manager.map_bar_list:
            if not map_bar.is_viewed:
                continue
            current_map_bar_clicked = map_bar.check_if_clicked()
            if not map_bar_clicked:
                map_bar_clicked = current_map_bar_clicked
        return map_bar_clicked
