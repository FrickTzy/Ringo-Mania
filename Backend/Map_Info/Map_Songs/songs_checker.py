from glob import glob


class SongChecker:
    def __init__(self):
        self.__path = "Backend/Songs"

    def get_all_songs(self):
        return [song.removesuffix(".mp3") for song in glob("*.mp3", root_dir=self.__path)]
