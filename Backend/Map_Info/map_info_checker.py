import requests
from bs4 import BeautifulSoup


class MapInfoChecker:
    def __init__(self):
        self.__path: str = "Backend/Map_Info/song_info.rinf"
        self.__web_parser = WebParser()
        self.current_song_info = {}
        self.__all_song_info = []

    def __set_current_song_info(self, song_info):
        exec(f"self.current_song_info = {song_info}")
        return self.current_song_info

    def __check_current_song_info(self, song_name: str):
        self.__all_song_info.append(self.current_song_info)
        if self.current_song_info.get(song_name) is not None:
            return self.current_song_info[song_name]["artist"]
        return False

    def get_song_artist(self, song_name: str):
        self.__reset()
        if retrieved_song_artist := self.__check_file(song_name=song_name):
            return retrieved_song_artist
        return self.__search_for_song_artist(song_name=song_name)

    def __check_file(self, song_name):
        with open(self.__path, 'r', errors="ignore", encoding="utf-8") as file:
            for song_info in file:
                self.__set_current_song_info(song_info=song_info)
                if artist := self.__check_current_song_info(song_name=song_name):
                    return artist
        return False

    def __search_for_song_artist(self, song_name: str):
        result = self.__web_parser.search(search=f"who made the song {song_name}")
        song_info = {song_name: {"artist": f"{result}"}}
        self.__all_song_info.append(song_info)
        self.__overwrite_file()
        return result

    def __overwrite_file(self):
        with open(self.__path, 'w', errors="ignore", encoding="utf-8") as file:
            for song_info in self.__all_song_info:
                file.writelines(f"{str(song_info)}\n")

    def __reset(self):
        self.__all_song_info.clear()
        self.current_song_info.clear()


class WebParser:
    def __init__(self):
        self.__url_template = "https://www.google.com/search?q="

    def search(self, search="is earth round?"):
        req = requests.get(url=f"{self.__url_template}{search}")
        parser = BeautifulSoup(req.text, "html.parser")
        result = parser.find("div", class_="BNeawe").text
        return result[:100]


if __name__ == "__main__":
    map_info_checker = MapInfoChecker()
