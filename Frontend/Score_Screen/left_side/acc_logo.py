from pygame import transform, image, Surface
from os import path


class AccLogo:
    __HIDE_PERFECT = False

    def __init__(self, screen_pos, opacity):
        self.__pos = AccLogoPos(screen_pos=screen_pos)
        self.__opacity = opacity
        self.__miss_img = transform.scale(
            image.load(path.join("Frontend\Mania_Window\Img", "hit0.png")).convert_alpha(),
            self.__pos.logo_size_tuple)
        self.__okay_img = transform.scale(
            image.load(path.join("Frontend\Mania_Window\Img", "hit50.png")).convert_alpha(),
            self.__pos.logo_size_tuple)
        self.__good_img = transform.scale(
            image.load(path.join("Frontend\Mania_Window\Img", "hit100.png")).convert_alpha(),
            self.__pos.logo_size_tuple)
        self.__perfect_img = transform.scale(
            image.load(path.join("Frontend\Mania_Window\Img", "hit300.png")).convert_alpha(),
            self.__pos.logo_size_tuple)
        self.__amazing_img = transform.scale(
            image.load(path.join("Frontend\Mania_Window\Img", "hit320.png")).convert_alpha(),
            self.__pos.logo_size_tuple)

    def show_logo(self, screen_surface: Surface):
        self.__set_logo_opacity()
        self.__blit_logo(screen_surface=screen_surface)

    def __blit_logo(self, screen_surface: Surface):
        screen_surface.blit(self.__amazing_img, self.__pos.right_logo_pos(sequence_num=1))
        screen_surface.blit(self.__perfect_img, self.__pos.left_logo_pos(sequence_num=1))
        screen_surface.blit(self.__good_img, self.__pos.right_logo_pos(sequence_num=2))
        screen_surface.blit(self.__okay_img, self.__pos.left_logo_pos(sequence_num=2))
        screen_surface.blit(self.__miss_img, self.__pos.center_logo_pos(sequence_num=3))

    def __set_logo_opacity(self):
        self.__amazing_img.set_alpha(self.__opacity.opacity)
        self.__perfect_img.set_alpha(self.__opacity.opacity)
        self.__good_img.set_alpha(self.__opacity.opacity)
        self.__okay_img.set_alpha(self.__opacity.opacity)
        self.__miss_img.set_alpha(self.__opacity.opacity)

    def __update_logo_size(self):
        self.__miss_img = transform.scale(
            self.__miss_img,
            self.__pos.logo_size_tuple)
        self.__okay_img = transform.scale(
            self.__okay_img,
            self.__pos.logo_size_tuple)
        self.__good_img = transform.scale(
            self.__good_img,
            self.__pos.logo_size_tuple)
        self.__perfect_img = transform.scale(
            self.__perfect_img,
            self.__pos.logo_size_tuple)
        self.__amazing_img = transform.scale(
            self.__amazing_img,
            self.__pos.logo_size_tuple)


class AccLogoPos:
    __Y_START_RATIO = 4.46
    __Y_INTERVAL_RATIO = 5.45
    __LEFT_X_RATIO = 16
    __RIGHT_X_RATIO = 3.59
    __CENTER_X_RATIO = 6.27
    __LOGO_SIZE_RATIO = 11.25

    def __init__(self, screen_pos):
        self.__screen_pos = screen_pos

    def left_logo_pos(self, sequence_num: int) -> tuple[int, int]:
        return self.__left_logo_x, self.__y_start + (sequence_num - 1) * self.__y_interval

    def right_logo_pos(self, sequence_num: int) -> tuple[int, int]:
        return self.__right_logo_x, self.__y_start + (sequence_num - 1) * self.__y_interval

    def center_logo_pos(self, sequence_num: int):
        return self.__center_logo_x, self.__y_start + (sequence_num - 1) * self.__y_interval

    @property
    def __left_logo_x(self):
        return self.__screen_pos.width // self.__LEFT_X_RATIO

    @property
    def __right_logo_x(self):
        return self.__screen_pos.width // self.__RIGHT_X_RATIO

    @property
    def __center_logo_x(self):
        return self.__screen_pos.width // self.__CENTER_X_RATIO

    @property
    def __y_start(self):
        return self.__screen_pos.height // self.__Y_START_RATIO

    @property
    def __y_interval(self):
        return self.__screen_pos.height // self.__Y_INTERVAL_RATIO

    @property
    def __logo_size(self):
        return self.__screen_pos.height // self.__LOGO_SIZE_RATIO

    @property
    def logo_size_tuple(self):
        return self.__logo_size, self.__logo_size
