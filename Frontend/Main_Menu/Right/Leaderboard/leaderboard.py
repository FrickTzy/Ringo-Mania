from .Record import Record
from pygame import Surface


class Leaderboard:
    __initialized = False
    __MAX_RECORD_VIEW = 6

    def __init__(self, play_tracker, display, state):
        self.__play_tracker = play_tracker
        self.__display = display
        self.__pos = Pos(display=display)
        self.__record_list: list[Record] = []
        self.__state = state
        self.__best_play: Record
        self.__img_surface = Surface((700, 50))

    def show_leaderboard(self, main_menu_surface, background_img):
        self.__init_leaderboard()
        self.__show_all_records(main_menu_surface=main_menu_surface, background_img=background_img)

    def __show_all_records(self, main_menu_surface, background_img):
        self.__img_surface.blit(background_img, (-1000, -635))
        self.__best_play.show(main_menu_surface=main_menu_surface, y=470)
        for index, record in enumerate(self.__record_list):
            if index == self.__MAX_RECORD_VIEW:
                main_menu_surface.blit(self.__img_surface, (1000, 635))
                return
            record.show(main_menu_surface=main_menu_surface, y=self.__pos.starting_record_pos(index=index))

    def __init_leaderboard(self):
        if self.__initialized:
            return
        play_list = self.__play_tracker.check_plays()
        self.__best_play = Record(play_dict=play_list[0], display=self.__display, state=self.__state)
        for play in play_list:
            self.__record_list.append(Record(play_dict=play, display=self.__display, state=self.__state))
        self.__initialized = True

    def restart(self):
        self.__initialized = False


class Pos:
    def __init__(self, display):
        self.__display = display

    def starting_record_pos(self, index):
        return index * 70
