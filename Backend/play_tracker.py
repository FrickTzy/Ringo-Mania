from os import path


class PlayTracker:
    SORT_TYPE = "score"

    def __init__(self, map_info):
        self.map_info = map_info
        self.updated = False
        self.sorted_plays: list = []
        self.converted_dict = {}

    @property
    def path(self):
        return path.join("Backend\Map_History", f"{self.map_info.song_name}.rinh")

    def check_plays(self) -> list:
        plays_history = []
        if not path.exists(self.path):
            return plays_history
        with open(self.path, 'r') as file:
            for plays in file:
                converted_dict = self.string_to_dict(plays)
                plays_history.append(converted_dict)
        return plays_history

    def update_plays(self, record: dict):
        if self.updated:
            return
        plays_history = self.check_plays()
        plays_history.append(record)
        self.sort_plays(plays_history)
        with open(self.path, 'w') as file:
            for plays in self.sorted_plays:
                file.writelines(f"{str(plays)}\n")
        self.updated = True

    def string_to_dict(self, plays):
        exec(f"self.converted_dict = {plays}")
        return self.converted_dict

    def sort_plays(self, plays_history: list[dict]):
        if len(plays_history) == 0:
            return
        max_score = 0
        current_max_scorer = ""
        for plays in plays_history:
            if (score := plays[self.SORT_TYPE]) > max_score:
                max_score = score
                current_max_scorer = plays
        self.sorted_plays.append(current_max_scorer)
        plays_history.pop(plays_history.index(current_max_scorer))
        self.sort_plays(plays_history)

    def reset_plays(self):
        with open(self.path, 'w') as file:
            file.writelines("")


if __name__ == "__main__":
    play_history = PlayTracker("Wotakoi")
    play_history.update_plays(
        {'score': 2667201, 'combo': 65, 'highest_combo': 118, 'date': '17/10/2023', 'time': '8:37 pm'})
