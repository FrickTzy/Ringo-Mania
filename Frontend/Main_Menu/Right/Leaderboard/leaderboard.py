from .Record import Record


class Leaderboard:
    __initialized = False

    def __init__(self, play_tracker, display, state):
        self.__play_tracker = play_tracker
        self.__display = display
        self.__pos = Pos(display=display)
        self.__play_list: list = []
        self.__record_list: list[Record] = []
        self.__state = state

    def show_leaderboard(self, main_menu_surface):
        self.__init_leaderboard()
        self.__show_all_records(main_menu_surface=main_menu_surface)

    def __show_all_records(self, main_menu_surface):
        for index, record in enumerate(self.__record_list):
            record.show(main_menu_surface=main_menu_surface, y=self.__pos.starting_record_pos(index=index))

    def __init_leaderboard(self):
        if self.__initialized:
            return
        self.__play_list = self.__play_tracker.check_plays()
        for play in self.__play_list:
            self.__record_list.append(Record(play_dict=play, display=self.__display, state=self.__state))
        self.__initialized = True

    def change_play_list(self):
        self.__play_list.clear()


class Pos:
    def __init__(self, display):
        self.__display = display

    def starting_record_pos(self, index):
        return index * 70
