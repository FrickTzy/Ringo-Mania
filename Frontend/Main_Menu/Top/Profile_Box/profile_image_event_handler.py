from Frontend.Helper_Files import ButtonEventHandler
import webbrowser


class ProfileImageEventHandler:
    __PROFILE_URL = "https://osu.ppy.sh/users/27211227"
    __already_pressed_profile = False

    def __init__(self):
        self.__button_handler = ButtonEventHandler()

    def check_if_click(self, starting_pos: tuple, size: tuple):
        pressed_profile = self.__button_handler.check_buttons_for_clicks(starting_pos=starting_pos,
                                                                         size=size)
        if not pressed_profile:
            self.__already_pressed_profile = False
            return
        if pressed_profile and not self.__already_pressed_profile:
            self.__open_profile_info()
            self.__already_pressed_profile = True

    def __open_profile_info(self):
        webbrowser.open(self.__PROFILE_URL)
