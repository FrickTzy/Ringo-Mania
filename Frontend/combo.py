from pygame import font as pyfont
from datetime import datetime
from Stuff.Ringo_Mania.Frontend.settings import PURPLE, MAX_LIFE, LIFE_INCREASE, LIFE_DMG, WHITE, GRADE_ACC, \
    COMBO_DIVIDER, OKAY_lIFE_DMG


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

    def __init__(self, font):
        self.fonts = font
        self.__info = ComboInfo()
        self.__life = MAX_LIFE
        self.date = ""
        self.current_time = ""
        self.accuracy: float = 0
        self.missed = False
        self.total_clicked: list[int] = []

    def miss_score(self, amount_of_circles) -> None:
        if amount_of_circles <= 0:
            return
        self.missed = True
        self.combo = 0
        self.add_clicked_circles(0)
        self.lose_life()
        self.miss_score(amount_of_circles - 1)

    def hit_circle_successfully(self, grade, acc, score):
        self.combo += 1
        self.compute_score(score)
        self.add_clicked_circles(acc)
        if grade == "Okay":
            self.lose_life(OKAY_lIFE_DMG)
            return
        if self.__life < MAX_LIFE:
            self.compute_life()

    @property
    def get_play_info(self):
        self.info.compute_highest_combo()
        self.compute_accuracy()
        return self.fonts.main_font.render(f"{self.info.combo}x", True, PURPLE), \
               self.fonts.main_font.render(f"{self.info.combo}", True, WHITE), \
               self.fonts.main_font.render(f"{self.info.score:08d}", True, PURPLE), \
               self.fonts.acc_font.render(f"{self.accuracy}%", True, PURPLE), \
               self.fonts.main_font.render(f"{self.life}", True, PURPLE)

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

    def get_grade(self):
        for grade, acc in GRADE_ACC.items():
            if self.accuracy >= acc:
                if grade == "S":
                    if not self.missed:
                        return grade
                    else:
                        continue
                return grade
        return "F"

    def add_clicked_circles(self, accuracy: int):
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

    def get_date(self):
        date = datetime.now()
        self.date = f"{date.day}/{date.month}/{date.year}"
        hour, pm = self.convert_to_standard_time(date.hour)
        self.current_time = f"{hour}:{self.fix_minutes(date.minute)} {pm}"

    @staticmethod
    def fix_minutes(minutes):
        if minutes < 10:
            return f"0{minutes}"
        return minutes

    @staticmethod
    def convert_to_standard_time(hour):
        if hour < 1:
            return 12, "am"
        elif hour < 12:
            return hour, "am"
        elif hour == 12:
            return hour, "pm"
        else:
            return hour - 12, "pm"

    def reset_all(self):
        self.__info.reset()
        self.__life = MAX_LIFE
        self.accuracy = 0
        self.missed = False
        self.total_clicked.clear()

    def get_stats(self):
        self.get_date()
        return {"score": self.info.score, "accuracy": f"{self.accuracy}%", "combo": self.info.combo,
                "highest_combo": self.info.highest_combo, "grade": f"{self.get_grade()}", "date": self.date,
                "time": self.current_time}


if __name__ == "__main__":
    counter = ComboCounter()
    counter.accuracy = 59
    print(counter.get_grade())
