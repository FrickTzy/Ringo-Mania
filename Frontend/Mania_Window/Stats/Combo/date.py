from datetime import datetime


class Date:
    def __init__(self):
        self.date = ""
        self.current_time = ""

    def update_date_and_time(self):
        date = datetime.now()
        self.date = f"{date.day:02d}/{date.month:02d}/{date.year}"
        hour, pm = self.convert_to_standard_time(date.hour)
        self.current_time = f"{hour}:{self.fix_minutes(date.minute)} {pm}"

    @property
    def get_date(self):
        self.update_date_and_time()
        return self.date

    @property
    def get_time(self):
        self.update_date_and_time()
        return self.current_time

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

    @staticmethod
    def fix_minutes(minutes):
        if minutes < 10:
            return f"0{minutes}"
        return minutes
