import pygame
import os


class ShowAcc:
    __HEIGHT_Y_RATIO = 2.3
    __ACC_IMG_SIZE = 80
    __HIDE_PERFECT = False
    __ACC_IMG_WIDTH, __ACC_IMG_HEIGHT = __ACC_IMG_SIZE, __ACC_IMG_SIZE

    def __init__(self):
        self.__acc = None
        self.miss_img = pygame.transform.scale(
            pygame.image.load(os.path.join("Frontend\Img", "hit0.png")).convert_alpha(),
            (self.__ACC_IMG_WIDTH, self.__ACC_IMG_HEIGHT))
        self.okay_img = pygame.transform.scale(
            pygame.image.load(os.path.join("Frontend\Img", "hit50.png")).convert_alpha(),
            (self.__ACC_IMG_WIDTH, self.__ACC_IMG_HEIGHT))
        self.good_img = pygame.transform.scale(
            pygame.image.load(os.path.join("Frontend\Img", "hit100.png")).convert_alpha(),
            (self.__ACC_IMG_WIDTH, self.__ACC_IMG_HEIGHT))
        self.perfect_img = pygame.transform.scale(
            pygame.image.load(os.path.join("Frontend\Img", "hit300.png")).convert_alpha(),
            (self.__ACC_IMG_WIDTH, self.__ACC_IMG_HEIGHT))
        self.amazing_img = pygame.transform.scale(
            pygame.image.load(os.path.join("Frontend\Img", "hit320.png")).convert_alpha(),
            (self.__ACC_IMG_WIDTH, self.__ACC_IMG_HEIGHT))
        self.acc_dict = {
            0: self.miss_img,
            50: self.okay_img,
            100: self.good_img,
            300: self.perfect_img,
            320: self.amazing_img,
        }

    def update_acc(self, acc):
        if self.__HIDE_PERFECT:
            if acc >= 300:
                acc = None
        self.__acc = acc

    def reset_acc(self):
        self.__acc = None

    def show_acc(self, window: pygame.Surface, window_size):
        if self.__acc is None:
            return
        window.blit(self.acc_dict[self.__acc], (self.get_coord(window_size=window_size)))

    def get_coord(self, window_size: tuple[int, int]):
        width, height = window_size
        return self.acc_identifier_x(width=width), self.acc_identifier_y(height=height)

    def acc_identifier_x(self, width):
        return width / 2 - (self.__ACC_IMG_SIZE / 2)

    def acc_identifier_y(self, height):
        return height // self.__HEIGHT_Y_RATIO
