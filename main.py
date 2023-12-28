from Backend import Music, Timer, MapManager, PlayTracker, MapInfo
from Frontend.Mania_Window import ManiaPlayWindow


class Main:
    def __init__(self):
        self.music = Music()
        self.timer = Timer()
        self.map_info = MapInfo(song_name="Torete")
        self.play_tracker = PlayTracker(self.map_info.song_name)
        self.play_window = ManiaPlayWindow(self.music, self.timer, MapManager, self.play_tracker,
                                           map_info=self.map_info)

    def run(self):
        self.play_window.run()


if __name__ == "__main__":
    main = Main()
    main.run()
