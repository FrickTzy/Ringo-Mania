from .profile_image import ProfileImage
from .profile_box_text import ProfileBoxText
from Frontend.Settings import PLAYER_NAME


class ProfileBox:
    __PLAYER_NAME = PLAYER_NAME

    def __init__(self, image_manager, display, player_tracker):
        self.__player_info = player_tracker.get_player_info(player_name=self.__PLAYER_NAME)
        self.__profile_box_pos = ProfileBoxPos(display=display)
        self.__profile_text = ProfileBoxText(display=display, player_info=self.__player_info,
                                             profile_box_pos=self.__profile_box_pos)
        self.__profile_image = ProfileImage(image_manager=image_manager, player_name=self.__PLAYER_NAME,
                                            profile_box_pos=self.__profile_box_pos, display=display)

    def show(self, surface):
        self.__profile_image.show(surface=surface)
        self.__profile_text.show_text(surface=surface, profile_image_end_x=self.__profile_image.end_x)


class ProfileBoxPos:
    def __init__(self, display):
        self.__display = display

    @property
    def starting_x(self):
        return 20

    @property
    def starting_y(self):
        return 0
