class MapIndexManager:
    __current_map_index = 0

    @property
    def current_index(self):
        return self.__current_map_index

    def set_index(self, index):
        self.__current_map_index = index
