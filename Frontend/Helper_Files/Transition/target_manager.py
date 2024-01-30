class TargetManager:
    __target_value_range = 0
    __current_value = 0
    __target_value = 0

    def setup(self, current_value, target_value):
        """
        This should only be called once every change.
        """
        self.__target_value_range = target_value - current_value
        self.__current_value = current_value
        self.__target_value = target_value

    @property
    def target_value_range(self):
        return self.__target_value_range

    @property
    def current_value(self):
        return self.__current_value

    def check_if_equal_target_value(self, value):
        if value == self.__target_value:
            return True
        return False
