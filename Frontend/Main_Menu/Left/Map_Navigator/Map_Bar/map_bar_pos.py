class MapBarPos:
    def __init__(self, display, pos, index):
        self.__display = display
        self.__pos = pos
        self.__record_y = 0
        self.__index = index
        self.__current_width = self.record_width

    @property
    def record_width(self):
        return 700

    @property
    def record_height(self):
        return self.__pos.record_height

    @property
    def chosen_record_width(self):
        return self.__pos.chosen_record_width

    @property
    def record_size(self):
        return self.record_width, self.record_height

    def set_current_width(self, width):
        self.__current_width = width

    @property
    def current_map_bar_width(self):
        return self.__current_width

    @property
    def hover_width(self):
        return self.__current_width + (self.__current_width * 0.05)

    @property
    def chosen_map_bar_size(self):
        return self.chosen_record_width, self.record_height

    @property
    def height(self):
        return self.__display.height

    def set_record_y(self):
        self.__record_y = self.__pos.record_starting_y + self.__pos.starting_record_pos(index=self.__index)

    def set_record_y_filter(self, index):
        self.__record_y = self.__pos.filtered_starting_y + self.__pos.starting_record_pos(index=index)

    def reset_y(self):
        self.__record_y = 0

    @property
    def record_y(self):
        return self.__record_y

    @property
    def record_x(self):
        return self.__pos.leaderboard_x

    @property
    def record_starting_coord(self):
        return self.record_x, self.record_y

    @property
    def current_size(self):
        return self.__current_width, self.record_height
