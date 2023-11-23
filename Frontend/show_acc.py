import pygame
import os
from Stuff.Ringo_Mania.Frontend.settings import ACC_IMG_X, ACC_IMG_Y, ACC_IMG_WIDTH, ACC_IMG_HEIGHT, HIDE_PERFECT


class ShowAcc:
    def __init__(self):
        self.__acc = None
        self.miss_img = pygame.transform.scale(
            pygame.image.load(os.path.join("Frontend\Img", "hit0.png")).convert_alpha(),
            (ACC_IMG_WIDTH, ACC_IMG_HEIGHT))
        self.okay_img = pygame.transform.scale(
            pygame.image.load(os.path.join("Frontend\Img", "hit50.png")).convert_alpha(),
            (ACC_IMG_WIDTH, ACC_IMG_HEIGHT))
        self.good_img = pygame.transform.scale(
            pygame.image.load(os.path.join("Frontend\Img", "hit100.png")).convert_alpha(),
            (ACC_IMG_WIDTH, ACC_IMG_HEIGHT))
        self.perfect_img = pygame.transform.scale(
            pygame.image.load(os.path.join("Frontend\Img", "hit300.png")).convert_alpha(),
            (ACC_IMG_WIDTH, ACC_IMG_HEIGHT))
        self.amazing_img = pygame.transform.scale(
            pygame.image.load(os.path.join("Frontend\Img", "hit320.png")).convert_alpha(),
            (ACC_IMG_WIDTH, ACC_IMG_HEIGHT))
        self.acc_dict = {
            0: self.miss_img,
            50: self.okay_img,
            100: self.good_img,
            300: self.perfect_img,
            320: self.amazing_img,
        }

    def update_acc(self, acc):
        if HIDE_PERFECT:
            if acc >= 300:
                acc = None
        self.__acc = acc

    def show_acc(self, window: pygame.Surface, x=ACC_IMG_X, y=ACC_IMG_Y):
        if self.__acc is None:
            return
        window.blit(self.acc_dict[self.__acc], (x, y))
