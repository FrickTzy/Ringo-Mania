class FilteredSearchManager:
    def __init__(self, map_nav_pos, search_tracker, list_manager, view_counter):
        self.__search_tracker = search_tracker
        self.__list_manager = list_manager
        self.__view_counter = view_counter
        self.__pos = map_nav_pos

    def filter_map_bar(self, main_menu_surface):
        self.__check_if_search_changed()
        self.__show_filtered_map_bar(main_menu_surface=main_menu_surface)

    def __check_if_search_changed(self):
        if self.__search_tracker.changed:
            self.reset_filter()
            self.__reset_pos()
            self.__update_filtered_list()

    def __show_filtered_map_bar(self, main_menu_surface):
        top_view_index = self.__view_counter.filtered_top_view
        for index in range(top_view_index, top_view_index + self.__view_counter.MAX_BAR_VIEW):
            try:
                self.__list_manager.filtered_map_bar_list[index].show_filtered(main_menu_surface=main_menu_surface,
                                                                               index=index)
            except IndexError:
                break

    def __update_filtered_list(self) -> None:
        search = self.__search_tracker.current_search.lower()
        self.__list_manager.using_filter = True
        self.__init_filtered_map_bar_list(search=search)

    def __reset_pos(self):
        for map_bar in self.__list_manager.map_bar_list:
            map_bar.reset_pos()

    def __init_filtered_map_bar_list(self, search: str):
        self.__list_manager.filtered_map_bar_list = [map_bar for map_bar in self.__list_manager.map_bar_list if
                                                     search in map_bar.song_file_name.lower() or
                                                     search in map_bar.song_artist.lower()]

    def reset_filter(self):
        self.__pos.reset_filtered_y()
        self.__view_counter.reset_filtered_view()
