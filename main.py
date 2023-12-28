from Backend import Music, Timer, MapManager, PlayTracker, MapInfo
from Frontend.Mania_Window import ManiaPlayWindow
from Frontend.display import Display


class Main:
    def __init__(self):
        self.music = Music()
        self.timer = Timer()
        self.__display = Display()
        self.map_info = MapInfo(song_name="Torete")
        self.play_tracker = PlayTracker(self.map_info.song_name)
        self.play_window = ManiaPlayWindow(music=self.music, timer=self.timer, map_manager=MapManager,
                                           play_tracker=self.play_tracker,
                                           map_info=self.map_info, display=self.__display)

    def run(self):
        self.play_window.run()


if __name__ == "__main__":
    main = Main()
    main.run()
