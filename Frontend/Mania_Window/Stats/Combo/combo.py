from pygame import font as pyfont
from Frontend.Settings import Color, MAX_LIFE, LIFE_INCREASE, LIFE_DMG, GRADE_ACC, COMBO_DIVIDER, OKAY_lIFE_DMG, \
    PLAYER_NAME
from Frontend.Mania_Window.Stats.Combo.date import Date


class ComboInfo:
    def __init__(self, combo=0, highest_combo=0, score=0):
        self.combo = combo
        self.highest_combo = highest_combo
        self.score = score

    def compute_highest_combo(self):
        if self.combo > self.highest_combo:
            self.highest_combo = self.combo

    def reset(self):
        self.combo = 0
        self.highest_combo = 0
        self.score = 0


class ComboCounter:
    pyfont.init()
    __acc_dict = {
        "Miss": 0,
        "Okay": 0,
        "Good": 0,
        "Perfect": 0,
        "Amazing": 0
    }
    __PRIMARY_COLOR = Color.PURPLE
    __SECONDARY_COLOR = Color.WHITE

    def __init__(self, font):
        self.fonts = font
        self.__info = ComboInfo()
        self.__life = MAX_LIFE
        self.__date = Date()
        self.accuracy: float = 0
        self.missed = False
        self.__miss_sfx = False
        self.total_clicked: list[int] = []

    def miss_score(self, amount_of_circles) -> None:
        if amount_of_circles <= 0:
            return
        if self.combo != 0:
            self.__miss_sfx = True
        self.missed = True
        self.combo = 0
        self.add_clicked_circles(0, "Miss")
        self.lose_life()
        self.miss_score(amount_of_circles - 1)

    def hit_circle_successfully(self, grade, acc, score):
        self.combo += 1
        self.compute_score(score)
        self.add_clicked_circles(acc, grade)
        if grade == "Okay":
            self.lose_life(OKAY_lIFE_DMG)
            return
        if self.__life < MAX_LIFE:
            self.compute_life()

    @property
    def get_grade(self):
        if self.__failed:
            return "F"
        for grade, acc in GRADE_ACC.items():
            if self.accuracy >= acc:
                if grade == "S":
                    if not self.missed:
                        return grade
                    else:
                        continue
                return grade
        return "F"

    @property
    def __failed(self):
        return self.__life <= 0

    def add_clicked_circles(self, accuracy: int, category: str):
        self.__acc_dict[category] += 1
        self.total_clicked.append(accuracy)

    def compute_score(self, score: int = 10):
        if not (combo_multiplier := (int(self.info.combo / COMBO_DIVIDER))):
            combo_multiplier = 1
        self.info.score += int(combo_multiplier * score)

    def compute_life(self):
        self.__life += int(self.info.combo * LIFE_INCREASE)
        if self.__life > MAX_LIFE:
            self.__life = MAX_LIFE

    def lose_life(self, life=LIFE_DMG):
        self.__life -= life
        if self.__life < 0:
            self.__life = 0

    def compute_accuracy(self):
        if len(self.total_clicked) == 0:
            self.accuracy = 100.0
            return
        self.accuracy = round(sum(self.total_clicked) / len(self.total_clicked), 2)

    @property
    def __formatted_acc(self):
        if self.accuracy == 100:
            return self.accuracy
        return format(self.accuracy, '.2f')

    def reset_all(self):
        self.__info.reset()
        self.__life = MAX_LIFE
        self.accuracy = 0
        self.missed = False
        self.total_clicked.clear()
        self.__reset_acc_dict()

    def __reset_acc_dict(self):
        for category in self.__acc_dict.keys():
            self.__acc_dict[category] = 0

    @property
    def miss_sfx(self):
        return self.__miss_sfx

    @miss_sfx.setter
    def miss_sfx(self, value: bool):
        self.__miss_sfx = value

    @property
    def get_play_info_text(self):
        self.info.compute_highest_combo()
        self.compute_accuracy()
        return self.fonts.main_font.render(f"{self.info.combo}x", True, self.__PRIMARY_COLOR), \
               self.fonts.main_font.render(f"{self.info.combo}", True, self.__SECONDARY_COLOR), \
               self.fonts.main_font.render(f"{self.info.score:08d}", True, self.__PRIMARY_COLOR), \
               self.fonts.acc_font.render(f"{self.__formatted_acc}%", True, self.__PRIMARY_COLOR), \
               self.fonts.main_font.render(f"{self.life}", True, self.__PRIMARY_COLOR)

    @property
    def combo(self):
        return self.info.combo

    @combo.setter
    def combo(self, new_value):
        self.info.combo = new_value

    @property
    def info(self):
        return self.__info

    @property
    def life(self):
        return self.__life

    @property
    def amount_dict(self) -> dict:
        return self.__acc_dict

    @property
    def date_time(self) -> dict:
        return {"date": self.__date.get_date, "time": self.__date.get_time}

    @property
    def get_stats(self):
        return {"player_name": PLAYER_NAME, "score": self.info.score, "accuracy": f"{self.__formatted_acc}%",
                "acc_dict": self.__acc_dict,
                "combo": self.info.combo,
                "highest_combo": self.info.highest_combo, "grade": self.get_grade, "date": self.__date.get_date,
                "time": self.__date.get_time}
