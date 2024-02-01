from abc import ABC, abstractmethod


class AnimationInterface(ABC):
    @abstractmethod
    def change_y(self, going_up: bool, current_y):
        pass
