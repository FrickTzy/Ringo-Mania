from glob import glob


class SongChecker:
    def __init__(self):
        self.__path = "C:/Users/Admiin/PycharmProjects/Ringo-chan's codes/Stuff/Ringo_Mania/Backend/Songs"

    def get_all_songs(self):
        return glob("*.mp3", root_dir=self.__path)
