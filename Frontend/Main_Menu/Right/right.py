from Frontend.Main_Menu.Right.Leaderboard.leaderboard import Leaderboard


class Right:
    def __init__(self, play_tracker, display):
        self.__leaderboard = Leaderboard(play_tracker=play_tracker, display=display)

    def show(self, main_menu_surface):
        self.__leaderboard.show_leaderboard(main_menu_surface=main_menu_surface)
