import os
import requests
import magic
from urllib.request import Request, urlopen
from urllib.parse import quote


class MapImageDownloader:
    __POSSIBLE_EXTENSIONS = ('.jpeg', ".jpg")
    __MAP_SEARCH_PADDING = " Pc Wallpaper"

    def __init__(self, anime_path, other_path):
        self.__anime_path = anime_path
        self.__other_path = other_path

    @staticmethod
    def __download_page(url):
        try:
            headers = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                                     "(KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"}
            req = Request(url, headers=headers)
            response = urlopen(req)
            response_data = str(response.read())
            return response_data

        except Exception as exception:
            print(exception)
            exit(0)

    def download(self, sentence_to_search: str, anime_path: bool = True):
        title = sentence_to_search.title().replace("'S", "'s")
        sentence_to_search = f"{title}{self.__MAP_SEARCH_PADDING}"
        image_url_extension = '&biw=1536&bih=674&tbm=isch&sxsrf=ACYBGNSXXpS6YmAKUiLKKBs6xWb4uUY5gA:1581168823770&' \
                              'source=lnms&sa=X&ved=0ahUKEwioj8jwiMLnAhW9AhAIHbXTBMMQ_AUI3QUoAQ'
        url = 'https://www.google.com/search?q=' + quote(sentence_to_search.encode('utf-8')) + image_url_extension
        webpage_html = self.__download_page(url)
        image_url = self.__look_for_images(webpage_html=webpage_html)
        self.__write_image(image_url=image_url, title=sentence_to_search, anime_path=anime_path)

    def __look_for_images(self, webpage_html):
        end_object = -1
        occurrence = 0
        while True:
            new_line = webpage_html.find('"https://', end_object + 1)
            end_object = webpage_html.find('"', new_line + 1)

            buffer = webpage_html.find('\\', new_line + 1, end_object)
            if buffer != -1:
                image_url = (webpage_html[new_line + 1:buffer])
            else:
                image_url = (webpage_html[new_line + 1:end_object])
            if any(extension in image_url for extension in self.__POSSIBLE_EXTENSIONS):
                occurrence += 1
            if occurrence > 4:  # Maybe try checking for jpeg instead of occurrence
                return image_url

    def __write_image(self, image_url, title, anime_path: bool):
        req = requests.get(image_url, allow_redirects=True, timeout=None)
        path = self.__anime_path if anime_path else self.__other_path
        if 'html' not in str(req.content):
            mime = magic.Magic(mime=True)
            file_type = mime.from_buffer(req.content)
            file_extension = f'.{file_type.split("/")[1]}'
            if file_extension not in self.__POSSIBLE_EXTENSIONS:
                raise ValueError()
            file_name = f"{title.replace(self.__MAP_SEARCH_PADDING, '')}{file_extension}"
            with open(os.path.join(path, file_name), 'wb') as file:
                file.write(req.content)


if __name__ == "__main__":
    map_downloader = MapImageDownloader()
    map_downloader.download(sentence_to_search='Moonstar88')
