from .Record import Record
from pygame import Surface, event, MOUSEWHEEL
from Frontend.Helper_Files import ButtonEventHandler


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
        self.__hidden_background = HiddenBackground()
        self.__event_handler = LeaderboardEventHandler(record_list=self.__record_list, pos=self.__pos)

    def show_leaderboard(self, main_menu_surface, background_img):
        self.__init_leaderboard()
        self.__show_all_records(main_menu_surface=main_menu_surface, background_img=background_img)
        self.__event_handler.check_for_events()

    def __show_all_records(self, main_menu_surface, background_img):
        for index, record in enumerate(self.__record_list):
            record.show(main_menu_surface=main_menu_surface, y=self.__pos.starting_record_pos(index=index))
        if len(self.__record_list) >= self.__MAX_RECORD_VIEW:
            self.__best_play.show_static(main_menu_surface=main_menu_surface, y=690)
            self.__hidden_background.show(background_img=background_img, surface=main_menu_surface)

    def __init_leaderboard(self):
        if self.__initialized:
            return
        play_list = self.__play_tracker.check_plays()
        self.__best_play = Record(play_dict=play_list[0], display=self.__display, state=self.__state, pos=self.__pos)
        for play in play_list:
            self.__record_list.append(
                Record(play_dict=play, display=self.__display, state=self.__state, pos=self.__pos))
        self.__initialized = True

    def restart(self):
        self.__initialized = False


class HiddenBackground:
    def __init__(self):
        self.__img_surface_bottom = Surface((700, 55))
        self.__img_surface_top = Surface((700, 55))

    def show(self, background_img, surface):
        self.__blit_image(image=background_img)
        self.__blit_to_surface(surface=surface)

    def __blit_to_surface(self, surface):
        surface.blit(self.__img_surface_top, (1000, 165))
        surface.blit(self.__img_surface_bottom, (1000, 635))

    def __blit_image(self, image):
        self.__img_surface_top.blit(image, (-1000, -165))
        self.__img_surface_bottom.blit(image, (-1000, -635))


class LeaderboardEventHandler:
    def __init__(self, record_list: list[Record], pos):
        self.__record_list = record_list
        self.__pos = pos
        self.__button_event_handler = ButtonEventHandler()

    def check_for_events(self):
        self.__check_if_scroll()

    def __check_if_scroll(self):
        if not self.__button_event_handler.check_if_mouse_is_in_an_area(
                starting_pos=self.__pos.leaderboard_starting_pos,
                size=self.__pos.leaderboard_size):
            return
        for event_occur in event.get():
            if event_occur.type == MOUSEWHEEL:
                if event_occur.y > 0:
                    self.__pos.change_starting_y(add=True)
                else:
                    self.__pos.change_starting_y(add=False)


class Pos:
    __INTERVAL_PER_SCROLL = 8
    __RECORD_INTERVAL = 12.86

    def __init__(self, display):
        self.__display = display
        self.__record_starting_y = 220

    def starting_record_pos(self, index):
        return index * self.__get_interval_per_record

    @property
    def __get_interval_per_record(self):
        return self.__display.height // self.__RECORD_INTERVAL

    @property
    def __leaderboard_starting_y(self):
        return 220

    @property
    def leaderboard_x(self):
        return 1000

    @property
    def leaderboard_width(self):
        return 550

    @property
    def leaderboard_height(self):
        return 415

    @property
    def leaderboard_size(self):
        return self.leaderboard_width, self.leaderboard_height

    @property
    def record_starting_y(self):
        return self.__record_starting_y

    @property
    def leaderboard_starting_pos(self):
        return self.leaderboard_x, self.__leaderboard_starting_y

    def change_starting_y(self, add: bool):
        if add:
            self.__record_starting_y += self.__INTERVAL_PER_SCROLL
        else:
            self.__record_starting_y -= self.__INTERVAL_PER_SCROLL
