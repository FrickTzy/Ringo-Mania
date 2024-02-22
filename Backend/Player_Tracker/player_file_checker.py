import json
from glob import glob
from datetime import datetime


class PlayerFileChecker:
    __PATH = "Backend/Player_Tracker/Player_Info"

    def check_if_player_exist(self, player_name):
        player_list = [player.removesuffix(".rinp") for player in glob("*.rinp", root_dir=self.__PATH)]
        if player_name in player_list:
            return True
        else:
            return False

    def get_player_info(self, player_name):
        with open(f"{self.__PATH}/{player_name}.rinp", "r") as file:
            player_data = json.load(file)
        return player_data

    def create_new_player_file(self, player_name):
        with open(f"{self.__PATH}/{player_name}.rinp", "w") as file:
            json.dump(self.__get_new_player_json(player_name=player_name), file)

    def __get_new_player_json(self, player_name):
        return {'player_name': player_name, "level": 1, "accuracy": "100.00%", "rin_points": "0rp", "total_score": 0,
                "date_created": self.__get_date()}

    @staticmethod
    def __get_date():
        date = datetime.now()
        return f"{date.day:02d}/{date.month:02d}/{date.year}"
