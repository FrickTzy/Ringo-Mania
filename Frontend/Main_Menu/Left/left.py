from .Map_Navigator.map_navigator import MapNavigator


class Left:
    def __init__(self, display, map_info, state, search_tracker, notifier, sfx_manager):
        self.__map_navigator = MapNavigator(display=display, map_info=map_info, state=state,
                                            search_tracker=search_tracker, notifier=notifier, sfx_manager=sfx_manager)

    def show(self, main_menu_surface):
        self.__map_navigator.show(main_menu_surface=main_menu_surface)

    def update(self):
        self.__map_navigator.update()
