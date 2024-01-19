class MapIndexManager:
    __current_map_index = None
    __changed = False

    @property
    def current_index(self):
        return self.__current_map_index

    def set_index(self, index):
        self.__current_map_index = index
        self.set_change()

    @property
    def changed(self):
        changed = self.__changed
        self.__changed = False
        return changed

    def set_change(self):
        self.__changed = True
