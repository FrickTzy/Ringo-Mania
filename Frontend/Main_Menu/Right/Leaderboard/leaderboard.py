from .Record import Record, RecordProfileImage
from pygame import Surface
from Frontend.Helper_Files import ButtonEventHandler


class Leaderboard:
    __initialized = False
    __map_records_dict = {}

    def __init__(self, play_tracker, display, state, notifier, sfx_manager):
        self.__play_tracker = play_tracker
        self.__display = display
        self.__pos = Pos(display=display)
        self.__record_list: list[Record] = []
        self.__state = state
        self.__view_counter = ViewCounter()
        self.__best_play: Record
        self.__hidden_background = HiddenBackground()
        self.__event_handler = LeaderboardEventHandler(record_list=self.__record_list, pos=self.__pos,
                                                       view=self.__view_counter, notifier=notifier,
                                                       sfx_manager=sfx_manager)
        self.__profile_image = RecordProfileImage()

    def show_leaderboard(self, main_menu_surface, background_img):
        self.__init_leaderboard()
        self.__show_all_records(main_menu_surface=main_menu_surface, background_img=background_img)
        self.__event_handler.check_for_events()

    def __show_all_records(self, main_menu_surface, background_img):
        self.__view_counter.reset_view()
        for index, record in enumerate(self.__record_list):
            record.show(main_menu_surface=main_menu_surface, y=self.__pos.starting_record_pos(index=index))
            self.__view_counter.check_if_viewed(record=record)
        if len(self.__record_list) >= self.__view_counter.MAX_RECORD_VIEW:
            self.__best_play.show_static(main_menu_surface=main_menu_surface, y=690)
            self.__event_handler.check_if_click_best_record(record=self.__best_play)
            self.__hidden_background.show(background_img=background_img, surface=main_menu_surface)

    def __init_leaderboard(self):
        if self.__initialized:
            return
        if not (play_list := self.__get_records_without_checking_dict()):
            return
        self.__best_play = play_list["best play"]
        for record in play_list["all records"]:
            self.__record_list.append(record)
        self.__pos.reset_record_starting_y()
        self.change_record_size()
        self.__initialized = True

    def __get_records(self):
        if (name := self.__play_tracker.name) not in self.__map_records_dict:
            play_list = self.__play_tracker.check_plays()
            self.__map_records_dict[name] = self.__get_all_map_bars(play_list=play_list)
        return self.__map_records_dict[name]
    
    def __get_records_without_checking_dict(self):
        play_list = self.__play_tracker.check_plays()
        return self.__get_all_map_bars(play_list=play_list)

    def __get_all_map_bars(self, play_list):
        record_list = []
        if not play_list:
            return {}
        for play in play_list:
            record_list.append(Record(play_dict=play, display=self.__display, state=self.__state, pos=self.__pos,
                                      profile_image=self.__profile_image))
        return {
            "best play": Record(play_dict=play_list[0], display=self.__display, state=self.__state, pos=self.__pos,
                                profile_image=self.__profile_image),
            "all records": record_list
        }

    def change_record_size(self):
        if not self.__record_list:
            return
        self.__profile_image.set_size(self.__record_list[0].profile_size_tuple)

    def restart(self):
        self.__initialized = False
        self.__record_list.clear()


class ViewCounter:
    MAX_RECORD_VIEW = 6
    NUMBER_OF_RECORD_THAT_CANNOT_SCROLL = 4
    current_record_view = 0

    def reset_view(self):
        self.current_record_view = 0

    def check_if_viewed(self, record: Record):
        if record.is_viewed:
            self.current_record_view += 1


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
    def __init__(self, record_list: list[Record], pos, view: ViewCounter, notifier, sfx_manager):
        self.__record_list = record_list
        self.__view = view
        self.__pos = pos
        self.__notifier = notifier
        self.__sfx_manager = sfx_manager
        self.__button_event_handler = ButtonEventHandler()

    def check_for_events(self):
        self.__check_mouse_input_events()

    def __check_mouse_input_events(self):
        if not self.__check_mouse_pos_is_in_correct_position():
            return
        self.__check_if_scroll()
        self.__check_if_clicked_record()

    def __check_mouse_pos_is_in_correct_position(self):
        if self.__button_event_handler.check_if_mouse_is_in_an_area(
                starting_pos=self.__pos.leaderboard_starting_pos,
                size=self.__pos.leaderboard_size):
            return True
        return False

    def __check_if_clicked_record(self):
        record_clicked = False
        for record in self.__record_list:
            current_record_clicked = record.check_if_clicked()
            if not record_clicked:
                record_clicked = current_record_clicked
        if record_clicked:
            self.__sfx_manager.play_menu_hit()

    def check_if_click_best_record(self, record):
        if record.check_if_clicked_best_play(y=690):
            self.__sfx_manager.play_menu_hit()

    def __check_if_scroll(self):
        if self.__notifier.scrolled:
            self.__scroll(event_occur=self.__notifier.event)

    def __scroll(self, event_occur):
        if event_occur.y > 0:
            if self.__pos.record_starting_y >= 222:
                return
            self.__pos.change_starting_y(add=True)
        else:
            if self.__check_if_out_of_bound_scroll():
                return
            self.__pos.change_starting_y(add=False)

    def __check_if_out_of_bound_scroll(self):
        if not len(self.__record_list) >= self.__view.MAX_RECORD_VIEW:
            return True
        if self.__view.current_record_view <= self.__view.NUMBER_OF_RECORD_THAT_CANNOT_SCROLL:
            return True


class Pos:
    __SCROLL_SPEED = 30
    __RECORD_INTERVAL = 12.86

    def __init__(self, display):
        self.__display = display
        self.__record_starting_y = 222

    def starting_record_pos(self, index):
        return index * self.__get_interval_per_record

    @property
    def __get_interval_per_record(self):
        return self.__display.height // self.__RECORD_INTERVAL

    @property
    def __leaderboard_starting_y(self):
        return 222

    def reset_record_starting_y(self):
        self.__record_starting_y = self.__leaderboard_starting_y

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
            self.__record_starting_y += self.__SCROLL_SPEED
        else:
            self.__record_starting_y -= self.__SCROLL_SPEED
