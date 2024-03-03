from pygame import K_BACKSPACE, K_TAB, K_DOWN, K_UP, K_RETURN, K_LALT, K_RALT, K_KP_ENTER, K_RSHIFT, K_LSHIFT, \
    K_CAPSLOCK


class SearchTracker:
    __changed = False
    __FORBIDDEN_KEYS = [K_TAB, K_LALT, K_RALT, K_DOWN, K_UP, K_RETURN, K_KP_ENTER, K_LSHIFT, K_RSHIFT, K_CAPSLOCK]

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

    def remove_a_letter(self):
        if not self.__current_search:
            return
        self.__current_search = self.__current_search[:-1]

    def add_letter(self, event):
        if event.key in self.__FORBIDDEN_KEYS:
            return
        elif event.key == K_BACKSPACE:
            self.remove_a_letter()
        else:
            self.__current_search += event.dict.get("unicode", "")
        self.__changed = True
