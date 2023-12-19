from .map_info_checker import MapInfoChecker


class MapInfo:
    def __init__(self, song_name: str, song_artist: str = "IDK", map_maker: str = "Dudesalp"):
        self.__song_name = song_name
        self.__artist = song_artist
        self.__map_maker = map_maker
        self.__info_checker = MapInfoChecker()

    @property
    def song_name(self):
        return self.__song_name

    @property
    def song_artist(self):
        return self.__artist

    @property
    def map_maker(self):
        return self.__map_maker

    @property
    def song_info(self):
        return f"{self.__song_name} - {self.__artist}"
