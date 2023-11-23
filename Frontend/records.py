from Stuff.Ringo_Mania.Frontend.combo import ComboInfo
from Stuff.Ringo_Mania.Frontend.font import Font
from Stuff.Ringo_Mania.Frontend.settings import WHITE, NUM_OF_RECORD, PLAYER_NAME


class Record:
    def __init__(self, font: Font):
        self.record_list: list[ComboInfo] = []
        self.fonts = font

    def init_record(self, record: list):
        """Adds the record to a list"""
        for index in range(NUM_OF_RECORD):
            try:
                self.add_record(record[index])
            except IndexError:
                return

    def add_record(self, record: dict) -> None:
        self.record_list.append(
            ComboInfo(score=record["score"], combo=record["combo"], highest_combo=record["highest_combo"]))

    def show_record(self, current_record):
        rendered_record = []
        for i in range(len(self.record_list)):
            rendered_record.append(self.render_record(self.record_list[i]))
        rendered_record.append(self.render_record(current_record))
        return rendered_record

    def render_record(self, record: ComboInfo):
        return self.fonts.record_font.render('{:,}'.format(record.score), True, WHITE), \
               self.fonts.record_font.render(f"{record.highest_combo}x", True, WHITE), \
               self.fonts.record_font.render(f"{PLAYER_NAME}", True, WHITE)
