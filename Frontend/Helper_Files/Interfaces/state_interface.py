from abc import ABC, abstractmethod


class State(ABC):
    @abstractmethod
    def leave_score_screen(self):
        pass

