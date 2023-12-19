import requests
from bs4 import BeautifulSoup


class MapInfoChecker:
    def __init__(self):
        self.__path: str = "song_info.rinf"
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
        if retrieved_song_artist := self.__check_file(song_name=song_name):
            return retrieved_song_artist
        return self.__search_for_song_artist(song_name=song_name)

    def __check_file(self, song_name):
        with open(self.__path, 'r') as file:
            for song_info in file:
                self.__set_current_song_info(song_info=song_info)
                if artist := self.__check_current_song_info(song_name=song_name):
                    return artist
        return False

    def __search_for_song_artist(self, song_name: str):
        self.__web_parser.search(search=f"who is the song artist for {song_name}")
        with open(self.__path, 'w') as file:
            for song_info in self.__all_song_info:
                file.writelines(f"{str(song_info)}\n")


class WebParser:
    def __init__(self):
        self.__url_template = "https://www.google.com/search?q="

    def search(self, search="is earth round?"):
        req = requests.get(f"{self.__url_template}{search}")
        parser = BeautifulSoup(req.text, "html.parser")
        result = parser.find("div", class_="BNeawe").text
        return result


if __name__ == "__main__":
    map_info_checker = MapInfoChecker()
    print(map_info_checker.get_song_artist("Reviver"))
