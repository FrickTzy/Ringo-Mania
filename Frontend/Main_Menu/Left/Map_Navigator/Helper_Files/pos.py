class MapNavigatorPos:
    __SCROLL_SPEED = 60
    __RECORD_INTERVAL = 8.12

    def __init__(self, display):
        self.__display = display
        self.__record_starting_y = 127
        self.__filtered_starting_y = 127

    def starting_record_pos(self, index):
        return index * self.__get_interval_per_record

    @property
    def chosen_record_width(self):
        return 780

    @property
    def record_height(self):
        return 107

    @property
    def chosen_size(self):
        return self.chosen_record_width, self.record_height

    @property
    def __get_interval_per_record(self):
        return self.__display.height // self.__RECORD_INTERVAL

    @property
    def __leaderboard_starting_y(self):
        return 127

    def set_y(self, index):
        self.__record_starting_y = self.get_target_y(index=index)

    def get_target_y(self, index):
        return self.__leaderboard_starting_y - self.starting_record_pos(index=index)

    def set_exact_y(self, y):
        self.__record_starting_y = y

    @property
    def leaderboard_x(self):
        return 0

    @property
    def leaderboard_width(self):
        return 700

    @property
    def leaderboard_height(self):
        return 650

    @property
    def leaderboard_size(self):
        return self.leaderboard_width, self.leaderboard_height

    @property
    def record_starting_y(self):
        return self.__record_starting_y

    @property
    def filtered_starting_y(self):
        return self.__filtered_starting_y

    def reset_filtered_y(self):
        self.__filtered_starting_y = self.__leaderboard_starting_y

    @property
    def leaderboard_starting_pos(self):
        return self.leaderboard_x, self.__leaderboard_starting_y

    def change_starting_y(self, add: bool):
        if add:
            self.__record_starting_y += self.__SCROLL_SPEED
        else:
            self.__record_starting_y -= self.__SCROLL_SPEED

    def change_filtered_starting_y(self, add: bool):
        if add:
            self.__filtered_starting_y += self.__SCROLL_SPEED
        else:
            self.__filtered_starting_y -= self.__SCROLL_SPEED

    def set_exact_filtered_y(self, y):
        self.__filtered_starting_y = y

    def add_y(self, y):
        self.__record_starting_y += y

    def add_filtered_y(self, y):
        self.__filtered_starting_y += y

    def subtract_y(self, y):
        self.__record_starting_y -= y

    def subtract_filtered_y(self, y):
        self.__filtered_starting_y -= y

    @property
    def get_window_size(self):
        return self.__display.get_window_size

    @property
    def scrollable_area(self):
        return 780, self.leaderboard_height
