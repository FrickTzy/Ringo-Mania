from Frontend.Mania_Window.Stats.Combo.combo import ComboInfo
from Frontend.Mania_Window.Misc.font import Font
from Frontend.settings import WHITE, NUM_OF_RECORD, PLAYER_NAME


class Record:
    def __init__(self, font: Font, display):
        self.record_list: list[ComboInfo] = []
        self.fonts = font
        self.display = display
        self.__pos = RecordPos(display=display)

    def init_record(self, record: list):
        """Adds the record to a list"""
        self.record_list.clear()
        for index in range(NUM_OF_RECORD):
            try:
                self.add_record(record[index])
            except IndexError:
                return

    def add_record(self, record: dict) -> None:
        self.record_list.append(
            ComboInfo(score=record["score"], combo=record["combo"], highest_combo=record["highest_combo"]))

    def get_record(self, current_record):
        rendered_record = []
        for i in range(len(self.record_list)):
            rendered_record.append(self.render_record(self.record_list[i]))
        rendered_record.append(self.render_record(current_record))
        return rendered_record

    def render_record(self, record: ComboInfo):
        return self.fonts.record_font.render('{:,}'.format(record.score), True, WHITE), \
               self.fonts.record_font.render(f"{record.highest_combo}x", True, WHITE), \
               self.fonts.record_font.render(f"{PLAYER_NAME}", True, WHITE)

    def show_record(self, current_rec):
        for index, record in enumerate(self.get_record(current_record=current_rec)):
            score, combo, name = record
            self.display.window.blit(score, self.__pos.score_coord(index=index))
            self.display.window.blit(combo, self.__pos.combo_coord(index=index))
            self.display.window.blit(name, self.__pos.name_coord(index=index))


class RecordPos:
    __SCORE_PADDING_RATIO = 7.78
    __NUM_OF_RECORD = 4
    __RECORD_Y_RATIO = 2.8
    __NAME_Y_RATIO = 3.02
    __RECORD_Y_INTERVAL_RATIO = 14
    __RECORD_X = 20

    def __init__(self, display):
        self.display = display

    @property
    def record_x(self):
        return self.__RECORD_X

    @property
    def record_y(self):
        return self.display.height // self.__RECORD_Y_RATIO

    @property
    def name_y(self):
        return self.display.height // self.__NAME_Y_RATIO

    @property
    def record_y_interval(self):
        return self.display.height // self.__RECORD_Y_INTERVAL_RATIO

    @property
    def score_padding(self):
        return self.display.height // self.__SCORE_PADDING_RATIO

    def score_coord(self, index: int):
        return self.record_x, self.record_y + (index * self.record_y_interval)

    def combo_coord(self, index: int):
        return self.record_x + self.score_padding, self.record_y + (index * self.record_y_interval)

    def name_coord(self, index: int):
        return self.record_x, self.name_y + (index * self.record_y_interval)
