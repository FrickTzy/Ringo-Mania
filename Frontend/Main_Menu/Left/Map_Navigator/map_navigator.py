from random import shuffle
from Backend.Map_Info.Map_Songs.songs_checker import SongChecker
from .Map_Bar.map_bar import MapBar
from .Map_Bar.map_index_manager import MapIndexManager
from .Search_Bar import SearchBar
from .Event_Handler import MapNavigatorEventHandler


class MapNavigator:
    __initialized = False

    def __init__(self, map_info, display, state, search_tracker, notifier):
        self.__map_info = map_info
        self.__song_checker = SongChecker()
        self.__search_tracker = search_tracker
        self.__list_manager = MapBarListManager()
        self.__search_bar = SearchBar(display=display, search_tracker=search_tracker)
        self.__display = display
        self.__index_manager = MapIndexManager()
        self.__view_counter = ViewCounter()
        self.__pos = MapNavigatorPos(display=display)
        self.__state = state
        self.__event_handler = MapNavigatorEventHandler(list_manager=self.__list_manager, pos=self.__pos,
                                                        view=self.__view_counter, notifier=notifier)

    def show(self, main_menu_surface):
        self.__init_leaderboard()
        self.__check_if_change_index()
        self.__show_all_map_bar(main_menu_surface=main_menu_surface)
        self.__search_bar.show(surface=main_menu_surface, selected_map_bar_pos=self.__list_manager.map_bar_list[
            self.__index_manager.current_index].position, map_bar_size=self.__pos.chosen_size)
        self.__event_handler.check_for_events(current_index=self.__index_manager.current_index)
        self.__check_if_set_map_info_and_image()

    def __check_if_change_index(self):
        if self.__index_manager.changed:
            self.__set_top_view()
            self.__pos.set_y(index=self.__view_counter.current_top_view)

    def __show_all_map_bar(self, main_menu_surface):
        if self.__search_tracker.current_search:
            self.__filter_map_bar(main_menu_surface=main_menu_surface)
        else:
            self.__show_unfiltered_map_bar(main_menu_surface=main_menu_surface)

    def __show_unfiltered_map_bar(self, main_menu_surface):
        self.__reset_filter()
        self.__list_manager.using_filter = False
        top_view_index = self.__view_counter.current_top_view
        for index in range(top_view_index - 1, top_view_index + self.__view_counter.MAX_BAR_VIEW):
            try:
                self.__list_manager.map_bar_list[index].show(main_menu_surface=main_menu_surface)
            except IndexError:
                break

    def __reset_filter(self):
        self.__pos.reset_filtered_y()
        self.__view_counter.reset_filtered_view()

    def __filter_map_bar(self, main_menu_surface):
        if self.__search_tracker.changed:
            self.__reset_filter()
            self.__reset_pos()
        search = self.__search_tracker.current_search.lower()
        self.__list_manager.using_filter = True
        self.__init_filtered_map_bar_list(search=search)
        top_view_index = self.__view_counter.filtered_top_view
        for index in range(top_view_index, top_view_index + self.__view_counter.MAX_BAR_VIEW):
            try:
                self.__list_manager.filtered_map_bar_list[index].show_filtered(main_menu_surface=main_menu_surface,
                                                                               index=index)
            except IndexError:
                break

    def __reset_pos(self):
        for map_bar in self.__list_manager.map_bar_list:
            map_bar.reset_pos()

    def __init_filtered_map_bar_list(self, search: str):
        self.__list_manager.filtered_map_bar_list = [map_bar for map_bar in self.__list_manager.map_bar_list if
                                                     search in map_bar.song_file_name.lower() or
                                                     search in map_bar.song_artist.lower()]

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
            self.__list_manager.map_bar_list[middle_chosen_index].set_chosen()

    def __set_top_view(self):
        self.__view_counter.current_top_view = self.__index_manager.current_index - 2

    def __init_bar_list(self, song_list):
        for index, song in enumerate(song_list):
            self.__list_manager.map_bar_list.append(
                MapBar(song_name=song, play_rank="A", display=self.__display, pos=self.__pos,
                       state=self.__state, index=index, index_manager=self.__index_manager))

    @property
    def current_image(self):
        return self.__list_manager.map_bar_list[self.__index_manager.current_index].image

    def __check_if_set_map_info_and_image(self):
        current_song_name = self.__list_manager.map_bar_list[self.__index_manager.current_index].song_file_name
        if self.__map_info.song_file_name == current_song_name:
            return
        self.__set_map_info_and_image()

    def __set_map_info_and_image(self):
        current_image = self.__list_manager.map_bar_list[self.__index_manager.current_index].image
        current_song_name = self.__list_manager.map_bar_list[self.__index_manager.current_index].song_file_name
        self.__map_info.set_song_name(song_name=current_song_name)
        self.__map_info.set_background(image=current_image)

    def restart(self):
        self.__initialized = False
        self.__list_manager.map_bar_list.clear()

    def update(self):
        self.__index_manager.set_change()


class ViewCounter:
    MAX_BAR_VIEW = 8
    MAX_BAR_SCROLL = 4
    current_map_bar_view = 0
    current_top_view = 0
    filtered_top_view = 0

    def reset_view(self):
        self.current_map_bar_view = 0

    def check_if_viewed(self, map_bar: MapBar):
        if map_bar.is_viewed:
            self.current_map_bar_view += 1

    def reset_filtered_view(self):
        self.filtered_top_view = 0


class MapBarListManager:
    map_bar_list: list[MapBar] = []
    filtered_map_bar_list: list[MapBar] = []
    using_filter: bool = False


class MapNavigatorPos:
    __SCROLL_SPEED = 60
    __RECORD_INTERVAL = 8.12

    def __init__(self, display):
        self.__display = display
        self.__record_starting_y = 127
        self.__filtered_starting_y = 127

    def starting_record_pos(self, index):
        return index * self.__get_interval_per_record

    @property
    def chosen_record_width(self):
        return 780

    @property
    def record_height(self):
        return 107

    @property
    def chosen_size(self):
        return self.chosen_record_width, self.record_height

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
    def filtered_starting_y(self):
        return self.__filtered_starting_y

    def reset_filtered_y(self):
        self.__filtered_starting_y = self.__leaderboard_starting_y

    @property
    def leaderboard_starting_pos(self):
        return self.leaderboard_x, self.__leaderboard_starting_y

    def change_starting_y(self, add: bool):
        if add:
            self.__record_starting_y += self.__SCROLL_SPEED
        else:
            self.__record_starting_y -= self.__SCROLL_SPEED

    def change_filtered_starting_y(self, add: bool):
        if add:
            self.__filtered_starting_y += self.__SCROLL_SPEED
        else:
            self.__filtered_starting_y -= self.__SCROLL_SPEED
