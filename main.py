from Backend import Music, Timer, MapManager, PlayTracker
from Frontend.Mania_Window import ManiaPlayWindow


class Main:
    def __init__(self):
        self.music = Music()
        self.timer = Timer()
        self.chosen_song = "Hell's Paradise"
        self.play_tracker = PlayTracker(self.chosen_song)
        self.play_window = ManiaPlayWindow(self.music, self.timer, MapManager, self.play_tracker, self.chosen_song)

    def run(self):
        self.play_window.run()


if __name__ == "__main__":
    main = Main()
    main.run()
