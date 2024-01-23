from pygame import K_BACKSPACE, K_TAB, K_DOWN, K_UP


class SearchTracker:
    __changed = False

    def __init__(self):
        self.__current_search = ""

    @property
    def current_search(self):
        return self.__current_search

    @current_search.setter
    def current_search(self, value):
        self.__current_search = value

    @property
    def changed(self):
        changed = self.__changed
        self.__changed = False
        return changed

    def add_letter(self, event):
        if event.key == K_TAB:
            return
        elif event.key == K_DOWN or event.key == K_UP:
            return
        elif event.key == K_BACKSPACE:
            self.__current_search = self.__current_search[:-1]
        else:
            self.__current_search += event.dict.get("unicode", "")
        self.__changed = True
