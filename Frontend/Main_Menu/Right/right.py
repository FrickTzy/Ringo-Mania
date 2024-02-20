from Frontend.Main_Menu.Right.Leaderboard.leaderboard import Leaderboard


class Right:
    def __init__(self, play_tracker, display, state, notifier, sfx_manager, profile_image_manager):
        self.__leaderboard = Leaderboard(play_tracker=play_tracker, display=display, state=state, notifier=notifier,
                                         sfx_manager=sfx_manager, profile_image_manager=profile_image_manager)

    def show(self, main_menu_surface, background_img):
        self.__leaderboard.show_leaderboard(main_menu_surface=main_menu_surface, background_img=background_img)

    def restart(self):
        self.__leaderboard.restart()
