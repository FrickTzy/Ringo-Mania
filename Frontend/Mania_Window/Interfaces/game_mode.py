from abc import abstractmethod
from Frontend.Helper_Files import WindowInterface


class GameModeWindow(WindowInterface):
    def __init__(self, *, display, font, music, play_tracker, timer, play_state):
        self.display = display
        self.font = font
        self.music = music
        self.play_tracker = play_tracker
        self.timer = timer
        self.state = play_state

    @abstractmethod
    def run(self):
        pass
