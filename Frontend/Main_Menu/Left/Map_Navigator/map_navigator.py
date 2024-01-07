from Backend.Map_Info.Map_Songs.songs_checker import SongChecker
from .Map_Bar.map_bar import MapBar
from random import shuffle


class MapNavigator:
    __map_bar_list: list[MapBar] = []
    __current_map_index = 0
    __initialized = False

    def __init__(self, map_info, display, state):
        self.__map_info = map_info
        self.__song_checker = SongChecker()
        self.__display = display
        self.__pos = MapNavigatorPos(display=display)
        self.__state = state

    def show(self, main_menu_surface):
        self.__init_leaderboard()
        self.__show_all_map_bar(main_menu_surface=main_menu_surface)

    def __show_all_map_bar(self, main_menu_surface):
        for index, map_bar in enumerate(self.__map_bar_list):
            if index > 6:
                return
            map_bar.show(main_menu_surface=main_menu_surface, y=self.__pos.starting_record_pos(index=index))

    def __init_leaderboard(self):
        if self.__initialized:
            return
        if not (song_list := self.__song_checker.get_all_songs()):
            return
        for song in song_list:
            self.__map_bar_list.append(
                MapBar(song_name=song, play_rank="A", display=self.__display, pos=self.__pos,
                       state=self.__state))
        shuffle(self.__map_bar_list)
        self.__map_bar_list[2].set_chosen()
        self.__map_info.set_song_name(song_name=self.__map_bar_list[2].song_name)
        self.__initialized = True

    def restart(self):
        self.__initialized = False
        self.__map_bar_list.clear()


class MapNavigatorPos:
    __SCROLL_SPEED = 40
    __RECORD_INTERVAL = 8.12

    def __init__(self, display):
        self.__display = display
        self.__record_starting_y = 127

    def starting_record_pos(self, index):
        return index * self.__get_interval_per_record

    @property
    def __get_interval_per_record(self):
        return self.__display.height // self.__RECORD_INTERVAL

    @property
    def __leaderboard_starting_y(self):
        return 127

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
        return 127

    @property
    def leaderboard_starting_pos(self):
        return self.leaderboard_x, self.__leaderboard_starting_y

    def change_starting_y(self, add: bool):
        if add:
            self.__record_starting_y += self.__SCROLL_SPEED
        else:
            self.__record_starting_y -= self.__SCROLL_SPEED
