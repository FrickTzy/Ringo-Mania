from Backend.Map_Info.Map_Infos.map_info_checker import MapInfoChecker


class MapInfo:
    def __init__(self, song_name: str, song_artist: str = "IDK", map_maker: str = "Dudesalp"):
        self.__song_file_name = song_name
        self.__artist = song_artist
        self.__map_maker = map_maker
        self.__info_checker = MapInfoChecker()

    @property
    def song_file_name(self):
        return self.__song_file_name

    @property
    def song_name(self):
        return self.__check_for_anime_titles()

    @property
    def __anime_title(self):
        if "Op" in self.__song_file_name:
            index = self.__song_file_name.index("Op")
        else:
            index = self.__song_file_name.index("Ed")
        return self.__song_file_name[:index - 1]

    @property
    def map_background_status(self):
        if "-" not in self.__song_file_name:
            return self.song_artist, False
        else:
            return self.__anime_title, True

    def __check_for_anime_titles(self):
        if "-" not in self.__song_file_name:
            return self.__song_file_name
        index = self.__song_file_name.index("-")
        return self.__song_file_name[index + 2::]

    @property
    def song_artist(self):
        return self.__info_checker.get_song_artist(song_name=self.__song_file_name)

    @property
    def map_maker(self):
        return self.__map_maker

    @property
    def song_info(self):
        return f"{self.song_name} - {self.song_artist}"
