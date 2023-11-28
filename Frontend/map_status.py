class MapStatus:
    def __init__(self):
        self.__failed = False
        self.__map_finished = False

    @property
    def failed(self):
        return self.__failed

    @failed.setter
    def failed(self, value: bool):
        self.__failed = value

    @property
    def finished(self):
        return self.__map_finished

    @finished.setter
    def finished(self, value: bool):
        self.__map_finished = value

    @property
    def failed_or_finished(self) -> bool:
        return self.finished or self.failed
