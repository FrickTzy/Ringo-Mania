from pygame import transform, image, Surface
from os import path


class AccLogo:
    __HEIGHT_Y_RATIO = 2.3
    __ACC_IMG_SIZE = 85
    __HIDE_PERFECT = False
    __ACC_IMG_WIDTH, __ACC_IMG_HEIGHT = __ACC_IMG_SIZE, __ACC_IMG_SIZE

    def __init__(self, screen_pos, opacity):
        self.__pos = AccLogoPos(screen_pos=screen_pos)
        self.__opacity = opacity
        self.__miss_img = transform.scale(
            image.load(path.join("Frontend\Mania_Window\Img", "hit0.png")).convert_alpha(),
            (self.__ACC_IMG_WIDTH, self.__ACC_IMG_HEIGHT))
        self.__okay_img = transform.scale(
            image.load(path.join("Frontend\Mania_Window\Img", "hit50.png")).convert_alpha(),
            (self.__ACC_IMG_WIDTH, self.__ACC_IMG_HEIGHT))
        self.__good_img = transform.scale(
            image.load(path.join("Frontend\Mania_Window\Img", "hit100.png")).convert_alpha(),
            (self.__ACC_IMG_WIDTH, self.__ACC_IMG_HEIGHT))
        self.__perfect_img = transform.scale(
            image.load(path.join("Frontend\Mania_Window\Img", "hit300.png")).convert_alpha(),
            (self.__ACC_IMG_WIDTH, self.__ACC_IMG_HEIGHT))
        self.__amazing_img = transform.scale(
            image.load(path.join("Frontend\Mania_Window\Img", "hit320.png")).convert_alpha(),
            (self.__ACC_IMG_WIDTH, self.__ACC_IMG_HEIGHT))

    def show_logo(self, end_screen_surface: Surface):
        self.__set_logo_opacity()
        self.__blit_logo(end_screen_surface=end_screen_surface)

    def __blit_logo(self, end_screen_surface: Surface):
        end_screen_surface.blit(self.__amazing_img, self.__pos.right_logo_pos(sequence_num=1))
        end_screen_surface.blit(self.__perfect_img, self.__pos.left_logo_pos(sequence_num=1))
        end_screen_surface.blit(self.__good_img, self.__pos.right_logo_pos(sequence_num=2))
        end_screen_surface.blit(self.__okay_img, self.__pos.left_logo_pos(sequence_num=2))
        end_screen_surface.blit(self.__miss_img, self.__pos.center_logo_pos(sequence_num=3))

    def __set_logo_opacity(self):
        self.__amazing_img.set_alpha(self.__opacity.opacity)
        self.__perfect_img.set_alpha(self.__opacity.opacity)
        self.__good_img.set_alpha(self.__opacity.opacity)
        self.__okay_img.set_alpha(self.__opacity.opacity)
        self.__miss_img.set_alpha(self.__opacity.opacity)


class AccLogoPos:
    __Y_INTERVAL = 200
    __TOP_INTERVAL = 207

    def __init__(self, screen_pos):
        self.screen_pos = screen_pos

    def left_logo_pos(self, sequence_num: int) -> tuple[int, int]:
        return 80, self.__TOP_INTERVAL + (sequence_num - 1) * self.__Y_INTERVAL

    def right_logo_pos(self, sequence_num: int) -> tuple[int, int]:
        return 425, self.__TOP_INTERVAL + (sequence_num - 1) * self.__Y_INTERVAL

    def center_logo_pos(self, sequence_num: int):
        return 250, self.__TOP_INTERVAL + (sequence_num - 1) * self.__Y_INTERVAL
