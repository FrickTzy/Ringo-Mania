from .filter_search import FilteredSearchManager


class SearchManager:
    def __init__(self, map_nav_pos, search_tracker, list_manager, view_counter):
        self.__search_tracker = search_tracker
        self.__search_filter = FilteredSearchManager(map_nav_pos=map_nav_pos, search_tracker=search_tracker,
                                                     list_manager=list_manager, view_counter=view_counter)

    def check_if_search(self, main_menu_surface):
        if self.__search_tracker.current_search:
            self.__search_filter.filter_map_bar(main_menu_surface=main_menu_surface)
            return True
        return False

    def reset_search(self):
        self.__search_filter.reset_filter()
