from abc import ABC, abstractmethod


class SmoothingInterface(ABC):
    @staticmethod
    @abstractmethod
    def smooth_in_animation(seconds_time: float):
        pass
