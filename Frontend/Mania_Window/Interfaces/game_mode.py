from abc import ABC, abstractmethod


class GameModeWindow(ABC):
    def __init__(self, *, display, font, music, play_tracker, timer):
        self.display = display
        self.font = font
        self.music = music
        self.play_tracker = play_tracker
        self.timer = timer

    @abstractmethod
    def run(self):
        pass
