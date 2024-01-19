from .Map_Navigator.map_navigator import MapNavigator


class Left:
    def __init__(self, display, map_info, state):
        self.__map_navigator = MapNavigator(display=display, map_info=map_info, state=state)

    def show(self, main_menu_surface):
        self.__map_navigator.show(main_menu_surface=main_menu_surface)

    def update(self):
        self.__map_navigator.update()

    @property
    def current_background_image(self):
        return self.__map_navigator.current_image
