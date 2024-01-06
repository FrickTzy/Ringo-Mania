from Backend.Map_Info.Map_Image.map_image_downloader import MapImageDownloader
from Backend.Map_Info.Map_Songs.songs_checker import SongChecker
from Backend.Map_Info.Map_Infos.map_info import MapInfo
from os import path


class MapImage:
    def __init__(self):
        self.__anime_path = "Backend/Map_Images/Anime Background"
        self.__other_path = "Backend/Map_Images/Others"
        self.__downloader = MapImageDownloader(anime_path=self.__anime_path, other_path=self.__other_path)

    def get_image(self, title: str, anime_song: bool):
        if anime_song:
            return self.__get_anime_img(title=title)
        else:
            return self.__get_other_img(title=title)

    def __get_anime_img(self, title):
        if path.exists(img_path := self.__get_anime_path(anime_title=title)[0]) or path.exists(
                img_path := self.__get_anime_path(anime_title=title)[1]):
            return img_path
        self.__downloader.download(sentence_to_search=title)
        return self.__get_anime_path(anime_title=title)

    def __get_other_img(self, title):
        if path.exists(img_path := self.__get_other_path(artist=title)[0]) or path.exists(
                img_path := self.__get_other_path(artist=title)[1]):
            return img_path
        self.__downloader.download(sentence_to_search=title, anime_path=False)
        return self.__get_anime_path(anime_title=title)

    def __get_anime_path(self, anime_title: str):
        return path.join(self.__anime_path, f"{anime_title.title()}.jpeg"), \
               path.join(self.__anime_path, f"{anime_title.title()}.png")

    def __get_other_path(self, artist: str):
        return path.join(self.__other_path, f"{artist.title()}.jpeg"), \
               path.join(self.__other_path, f"{artist.title()}.png")


def _update_all_map_img():
    for songs in SongChecker().get_all_songs():
        if "-" not in songs and "Op" not in songs:
            song = songs.removesuffix(".mp3")
            map_img = MapInfo(song_name=song)
            print(map_image.get_image(title=map_img.song_artist, anime_song=False))
            continue
        if "Op" in songs:
            index = songs.index("Op")
        else:
            index = songs.index("Ed")
        song = songs[:index - 1]
        print(map_image.get_image(title=song, anime_song=True))


def _an_anime_song(song_title: str):
    if "-" not in song_title:
        return False
    return True


if __name__ == "__main__":
    map_image = MapImage()
    _update_all_map_img()
