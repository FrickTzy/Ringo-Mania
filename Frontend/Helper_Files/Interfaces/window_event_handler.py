from abc import ABC, abstractmethod


class WindowEventHandler(ABC):
    @abstractmethod
    def check_window_if_quit(self):
        pass
