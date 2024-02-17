from Backend.Map_Info.Map_Info.map_info import MapInfo


class MapBarInfo:
    def __init__(self, song_name, play_rank, star_rating=3.0):
        self.__map_info = MapInfo(song_name=song_name)
        self.__play_rank = play_rank
        self.__star_rating = star_rating

    @property
    def song_name(self):
        return self.__map_info.song_name

    @property
    def song_file_name(self):
        return self.__map_info.song_file_name

    @property
    def song_artist(self):
        return self.__map_info.song_artist

    @property
    def song_name_status(self):
        return self.__map_info.map_background_status
