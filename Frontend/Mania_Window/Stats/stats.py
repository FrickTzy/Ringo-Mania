from Frontend.Mania_Window.Stats.Show_Acc.life_bar import LifeBar


class Stats:
    __mid_combo_display = False

    def __init__(self, display):
        self.display = display
        self.life_bar = LifeBar(display=display)
        self.pos = StatsPos(display=display)

    def show_all(self, play_info: tuple, life):
        combo, mid_combo, score, acc, life_txt = play_info
        self.life_bar.show_life_bar(life=life)
        self.display.window.blit(combo, (self.pos.combo_x, self.pos.combo_pos_y))
        self.display.window.blit(score, (self.pos.score_pos_x, self.pos.score_y))
        self.display.window.blit(acc, (self.pos.acc_pos_x, self.pos.acc_y))
        if self.__mid_combo_display:
            self.display.window.blit(mid_combo, self.pos.mid_combo_pos)


class StatsPos:
    __COMBO_Y_PADDING = 70
    __COMBO_X = 20
    __ACC_X_PADDING = 115
    __SCORE_X_PADDING = 175
    __SCORE_Y = 15
    __ACC_Y_RATIO = 11.75
    __SCORE_X_RATIO = 4
    __ACC_X_RATIO = 6.09

    def __init__(self, display):
        self.display = display

    @property
    def combo_x(self):
        return self.__COMBO_X

    @property
    def score_y(self):
        return self.__SCORE_Y

    @property
    def combo_pos_y(self):
        return self.display.height - self.__COMBO_Y_PADDING

    @property
    def score_pos_x(self):
        return self.display.width - (self.display.height // self.__SCORE_X_RATIO)

    @property
    def acc_pos_x(self):
        return self.display.width - (self.display.height // self.__ACC_X_RATIO)

    @property
    def acc_y(self):
        return self.display.height // self.__ACC_Y_RATIO

    @property
    def mid_combo_pos(self):
        return self.display.center
