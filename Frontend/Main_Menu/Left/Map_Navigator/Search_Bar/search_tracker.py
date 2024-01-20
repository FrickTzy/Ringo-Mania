from pygame import K_BACKSPACE


class SearchTracker:
    def __init__(self):
        self.__current_search = ""

    @property
    def current_search(self):
        return self.__current_search

    @current_search.setter
    def current_search(self, value):
        self.__current_search = value

    def add_letter(self, event):
        if event.key == K_BACKSPACE:
            self.__current_search = self.__current_search[:-1]
        else:
            self.__current_search += event.dict.get("unicode", "")
