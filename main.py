from Frontend import PlayWindow
from Backend import Music, Timer, MapManager, PlayTracker


class Main:
    def __init__(self):
        self.music = Music()
        self.timer = Timer()
        self.chosen_song = "Show"
        self.play_tracker = PlayTracker(self.chosen_song)
        self.play_window = PlayWindow(self.music, self.timer, MapManager, self.play_tracker, self.chosen_song)

    def run(self):
        self.play_window.run()


if __name__ == "__main__":
    main = Main()
    main.run()

# pro
