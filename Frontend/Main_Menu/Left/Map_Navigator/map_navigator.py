from random import shuffle
from Backend.Map_Info.Map_Songs.songs_checker import SongChecker
from .Map_Bar import MapBar, MapIndexManager
from .Search_Bar import SearchBar
from .Event_Handler import MapNavigatorEventHandler
from .Search_Manager import SearchManager
from .Helper_Files import MapBarListManager, MapNavigatorPos, ViewCounter, HoverManager
from .Animation import AnimationManager, SmoothScroll
from Backend.Map_Info.Map_Infos.map_info import MapInfo


class MapNavigator:
    def __init__(self, map_info: MapInfo, display, state, search_tracker, notifier, sfx_manager):
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
        self.__hover_manager = HoverManager()
        self.__scroll_manager = SmoothScroll(list_manager=self.__list_manager, pos=self.__pos, view=self.__view_counter)
        self.__event_handler = MapNavigatorEventHandler(list_manager=self.__list_manager, pos=self.__pos,
                                                        notifier=notifier,
                                                        sfx_manager=sfx_manager, hover_manager=self.__hover_manager,
                                                        scroll_manager=self.__scroll_manager)
        self.__search_manager = SearchManager(map_nav_pos=self.__pos, search_tracker=search_tracker,
                                              list_manager=self.__list_manager,
                                              view_counter=self.__view_counter)
        self.__initializer = MapNavInitializer(map_info=map_info, song_checker=self.__song_checker,
                                               list_manager=self.__list_manager, display=display,
                                               index_manager=self.__index_manager, pos=self.__pos,
                                               view_counter=self.__view_counter, state=state,
                                               hover_manager=self.__hover_manager)
        self.__animation_manager = AnimationManager(view=self.__view_counter, pos=self.__pos,
                                                    list_manager=self.__list_manager)

    def show(self, main_menu_surface):
        self.__initializer.init_leaderboard()
        self.__check_if_change_index()
        self.__animation_manager.check_for_animation()
        self.__show_all_map_bar(main_menu_surface=main_menu_surface)
        self.__search_bar.show(surface=main_menu_surface, selected_map_bar_pos=self.__list_manager.map_bar_list[
            self.__index_manager.current_index].position, map_bar_size=self.__pos.chosen_size)
        self.__event_handler.check_for_events(current_index=self.__index_manager.current_index)
        self.__check_if_set_map_info_and_image()

    def __check_if_change_index(self):
        if not self.__initializer.initialized:
            self.__set_top_view()
            self.__pos.set_y(index=self.__view_counter.current_top_view)
            self.__initializer.set_initialized()
            return
        elif self.__index_manager.changed:
            self.__animation_manager.setup(current_index=self.__index_manager.current_index)

    def __show_all_map_bar(self, main_menu_surface):
        if self.__search_manager.check_if_search(main_menu_surface=main_menu_surface):
            return
        self.__show_unfiltered_map_bar(main_menu_surface=main_menu_surface)

    def __show_unfiltered_map_bar(self, main_menu_surface):
        self.__check_if_init()
        self.__search_manager.reset_search()
        self.__list_manager.using_filter = False
        top_view_index = self.__view_counter.current_top_view
        for index in range(top_view_index - 1, top_view_index + self.__view_counter.MAX_BAR_VIEW):
            try:
                self.__list_manager.map_bar_list[index].show(main_menu_surface=main_menu_surface)
            except IndexError:
                break

    def __check_if_init(self):
        if not self.__search_tracker.changed:
            return
        self.__set_top_view()
        self.__pos.set_y(index=self.__view_counter.current_top_view)
        self.__reset_pos()

    def __reset_pos(self):
        for map_bar in self.__list_manager.map_bar_list:
            map_bar.update_rect()

    def __set_top_view(self):
        self.__view_counter.current_top_view = self.__index_manager.current_index - 2

    def __check_if_set_map_info_and_image(self):
        current_song_name = self.__list_manager.map_bar_list[self.__index_manager.current_index].song_file_name
        if self.__map_info.song_file_name == current_song_name:
            return
        self.__initializer.set_map_info_and_image()

    def update(self):
        self.__index_manager.set_change()

    def __debug(self):
        print(self.__pos.record_starting_y, self.__pos.filtered_starting_y)


class MapNavInitializer:
    __initialized = False

    def __init__(self, map_info: MapInfo, song_checker, list_manager, display, index_manager, view_counter, state, pos,
                 hover_manager):
        self.__map_info = map_info
        self.__song_checker = song_checker
        self.__list_manager = list_manager
        self.__display = display
        self.__index_manager = index_manager
        self.__view_counter = view_counter
        self.__pos = pos
        self.__state = state
        self.__hover_manager = hover_manager

    def init_leaderboard(self):
        if self.__initialized:
            return
        if not (song_list := self.__song_checker.get_all_songs()):
            return
        shuffle(song_list)
        self.__init_bar_list(song_list=song_list)
        self.__set_index(len_of_song_list=len(song_list))
        self.set_map_info_and_image()
        self.__pos.set_y(index=self.__view_counter.current_top_view)

    def __init_bar_list(self, song_list):
        for index, song in enumerate(song_list):
            self.__append_list(index=index, song=song)

    def set_map_info_and_image(self):
        current_image = self.__list_manager.map_bar_list[self.__index_manager.current_index].image
        current_song_name = self.__list_manager.map_bar_list[self.__index_manager.current_index].song_file_name
        self.__map_info.set_song_name(song_name=current_song_name)
        self.__map_info.set_background(image=current_image, window_size=self.__pos.get_window_size)

    def __append_list(self, index, song):
        self.__list_manager.map_bar_list.append(
            MapBar(song_name=song, play_rank="A", display=self.__display, pos=self.__pos,
                   state=self.__state, index=index, index_manager=self.__index_manager,
                   hover_manager=self.__hover_manager))

    def __set_index(self, len_of_song_list):
        if self.__index_manager.current_index is None:
            middle_chosen_index = len_of_song_list // 2 + 2
            self.__list_manager.map_bar_list[middle_chosen_index].set_chosen()

    def reset_init(self):
        self.__initialized = False
        self.__list_manager.map_bar_list.clear()

    @property
    def initialized(self):
        return self.__initialized

    def set_initialized(self):
        self.__initialized = True
