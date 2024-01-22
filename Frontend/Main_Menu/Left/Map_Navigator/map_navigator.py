from pygame import MOUSEWHEEL, event, key, K_RSHIFT, K_UP, K_DOWN
from random import shuffle
from Backend.Map_Info.Map_Songs.songs_checker import SongChecker
from Backend.timer import IntervalTimer
from .Map_Bar.map_bar import MapBar
from .Map_Bar.map_index_manager import MapIndexManager
from Frontend.Helper_Files import ButtonEventHandler
from .Search_Bar import SearchBar


class MapNavigator:
    __map_bar_list: list[MapBar] = []
    __filtered_map_bar_list: list[MapBar] = []
    __initialized = False

    def __init__(self, map_info, display, state, search_tracker):
        self.__map_info = map_info
        self.__song_checker = SongChecker()
        self.__search_tracker = search_tracker
        self.__search_bar = SearchBar(display=display, search_tracker=search_tracker)
        self.__display = display
        self.__index_manager = MapIndexManager()
        self.__view_counter = ViewCounter()
        self.__pos = MapNavigatorPos(display=display)
        self.__state = state
        self.__event_handler = MapNavigatorEventHandler(map_bar_list=self.__map_bar_list, pos=self.__pos,
                                                        view=self.__view_counter)

    def show(self, main_menu_surface):
        self.__init_leaderboard()
        self.__check_if_change_index()
        self.__show_all_map_bar(main_menu_surface=main_menu_surface)
        self.__search_bar.show(surface=main_menu_surface)
        self.__event_handler.check_for_events(current_index=self.__index_manager.current_index)
        self.__check_if_set_map_info_and_image()

    def __check_if_change_index(self):
        if self.__index_manager.changed:
            self.__set_top_view()
            self.__pos.set_y(index=self.__view_counter.current_top_view)

    def __show_all_map_bar(self, main_menu_surface):
        top_view_index = self.__view_counter.current_top_view
        for index in range(top_view_index, top_view_index + self.__view_counter.MAX_BAR_VIEW):
            try:
                self.__map_bar_list[index].show(main_menu_surface=main_menu_surface,
                                                y=self.__pos.starting_record_pos(index=index))
            except IndexError:
                break

    def __filter_map_bar(self):
        pass

    def __init_leaderboard(self):
        if self.__initialized:
            return
        if not (song_list := self.__song_checker.get_all_songs()):
            return
        shuffle(song_list)
        self.__init_bar_list(song_list=song_list)
        self.__set_index(len_of_song_list=len(song_list))
        self.__set_map_info_and_image()
        self.__pos.set_y(index=self.__view_counter.current_top_view)
        self.__initialized = True

    def __set_index(self, len_of_song_list):
        if self.__index_manager.current_index is None:
            middle_chosen_index = len_of_song_list // 2 + 2
            self.__map_bar_list[middle_chosen_index].set_chosen()

    def __set_top_view(self):
        self.__view_counter.current_top_view = self.__index_manager.current_index - 2

    def __init_bar_list(self, song_list):
        for index, song in enumerate(song_list):
            self.__map_bar_list.append(
                MapBar(song_name=song, play_rank="A", display=self.__display, pos=self.__pos,
                       state=self.__state, index=index, index_manager=self.__index_manager))

    @property
    def current_image(self):
        return self.__map_bar_list[self.__index_manager.current_index].image

    def __check_if_set_map_info_and_image(self):
        current_song_name = self.__map_bar_list[self.__index_manager.current_index].song_file_name
        if self.__map_info.song_file_name == current_song_name:
            return
        self.__set_map_info_and_image()

    def __set_map_info_and_image(self):
        current_image = self.__map_bar_list[self.__index_manager.current_index].image
        current_song_name = self.__map_bar_list[self.__index_manager.current_index].song_file_name
        self.__map_info.set_song_name(song_name=current_song_name)
        self.__map_info.set_background(image=current_image)

    def restart(self):
        self.__initialized = False
        self.__map_bar_list.clear()

    def update(self):
        self.__index_manager.set_change()


class ViewCounter:
    MAX_BAR_VIEW = 8
    MAX_BAR_SCROLL = 4
    current_map_bar_view = 0
    current_top_view = 0

    def reset_view(self):
        self.current_map_bar_view = 0

    def check_if_viewed(self, map_bar: MapBar):
        if map_bar.is_viewed:
            self.current_map_bar_view += 1


class MapNavigatorEventHandler:
    __CLICK_INTERVAL = 80

    def __init__(self, map_bar_list: list[MapBar], pos, view: ViewCounter):
        self.__interval_timer: IntervalTimer = IntervalTimer(interval=self.__CLICK_INTERVAL)
        self.__map_bar_list = map_bar_list
        self.__view = view
        self.__pos = pos
        self.__button_event_handler = ButtonEventHandler()

    def check_for_events(self, current_index):
        self.__check_mouse_input_events()
        self.__check_keyboard_input_events(current_index=current_index)

    def __check_mouse_input_events(self):
        if not self.__check_mouse_pos_is_in_correct_position():
            return
        self.__check_if_scroll()
        self.__check_if_clicked_record()

    def __check_keyboard_input_events(self, current_index):
        key_pressed = key.get_pressed()
        self.__check_if_enter_key(key_pressed=key_pressed, map_bar=self.__map_bar_list[current_index])
        self.__check_if_enter_arrow_key(key_pressed=key_pressed)

    def __check_mouse_pos_is_in_correct_position(self):
        if self.__button_event_handler.check_if_mouse_is_in_an_area(
                starting_pos=self.__pos.leaderboard_starting_pos,
                size=self.__pos.leaderboard_size):
            return True
        return False

    def __check_if_clicked_record(self):
        if not self.__interval_timer.time_interval_finished():
            return
        for map_bar in self.__map_bar_list:
            map_bar.check_if_clicked()

    @staticmethod
    def __check_if_enter_key(key_pressed, map_bar):
        if key_pressed[K_RSHIFT]:
            map_bar.key_hit()

    def __check_if_enter_arrow_key(self, key_pressed):
        if key_pressed[K_UP]:
            self.__go_up()
        if key_pressed[K_DOWN]:
            self.__go_down()

    def __check_if_scroll(self):
        for event_occur in event.get():
            if event_occur.type == MOUSEWHEEL:
                self.__scroll(event_occur=event_occur)

    def __scroll(self, event_occur):
        if event_occur.y > 0:
            self.__go_up()
        else:
            self.__go_down()

    def __go_up(self):
        if self.__pos.record_starting_y >= 300:
            return
        self.__pos.change_starting_y(add=True)
        self.__check_current_bottom_view()

    def __go_down(self):
        if self.__view.current_top_view >= len(self.__map_bar_list) - self.__view.MAX_BAR_SCROLL:
            return
        self.__pos.change_starting_y(add=False)
        self.__check_current_top_view()

    def __check_if_out_of_bound_scroll(self):
        if not len(self.__map_bar_list) >= self.__view.MAX_BAR_VIEW:
            return True
        if self.__view.current_map_bar_view <= self.__view.MAX_BAR_SCROLL:
            return True

    def __check_current_top_view(self):
        if len(self.__map_bar_list) - 1 <= self.__view.current_top_view:
            return
        if not self.__map_bar_list[self.__view.current_top_view].is_viewed:
            self.__view.current_top_view += 1

    def __check_current_bottom_view(self):
        if self.__view.current_top_view == 0:
            return
        if self.__map_bar_list[self.__view.current_top_view].change_top_index:
            self.__view.current_top_view -= 1


class MapNavigatorPos:
    __SCROLL_SPEED = 60
    __RECORD_INTERVAL = 8.12

    def __init__(self, display):
        self.__display = display
        self.__record_starting_y = 127

    def starting_record_pos(self, index):
        return index * self.__get_interval_per_record

    @property
    def __get_interval_per_record(self):
        return self.__display.height // self.__RECORD_INTERVAL

    @property
    def __leaderboard_starting_y(self):
        return 127

    def set_y(self, index):
        self.__record_starting_y = self.__leaderboard_starting_y - self.starting_record_pos(index=index)

    @property
    def leaderboard_x(self):
        return 0

    @property
    def leaderboard_width(self):
        return 700

    @property
    def leaderboard_height(self):
        return 650

    @property
    def leaderboard_size(self):
        return self.leaderboard_width, self.leaderboard_height

    @property
    def record_starting_y(self):
        return self.__record_starting_y

    @property
    def leaderboard_starting_pos(self):
        return self.leaderboard_x, self.__leaderboard_starting_y

    def change_starting_y(self, add: bool):
        if add:
            self.__record_starting_y += self.__SCROLL_SPEED
        else:
            self.__record_starting_y -= self.__SCROLL_SPEED
