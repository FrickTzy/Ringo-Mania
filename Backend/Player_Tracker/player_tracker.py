from .player_file_checker import PlayerFileChecker


class PlayerTracker:
    def __init__(self):
        self.__file_checker = PlayerFileChecker()

    def __create_player_info(self, player_name):
        self.__file_checker.create_new_player_file(player_name=player_name)

    def get_player_info(self, player_name):
        if not self.__file_checker.check_if_player_exist(player_name=player_name):
            self.__create_player_info(player_name=player_name)
        return self.__file_checker.get_player_info(player_name=player_name)
