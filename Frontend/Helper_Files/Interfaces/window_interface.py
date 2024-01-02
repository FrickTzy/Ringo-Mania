from abc import ABC, abstractmethod


class WindowInterface(ABC):
    @abstractmethod
    def run(self):
        pass
