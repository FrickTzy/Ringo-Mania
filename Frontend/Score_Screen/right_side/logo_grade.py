from pygame import transform, image, Surface
from os import path


class LogoGrade:
    __current_size = 0
    __current_img = None
    __current_grade = None

    def __init__(self, pos):
        self.__pos = GradePosSize(pos=pos)
        self.__f_img = image.load(path.join("Frontend\Mania_Window\Img", "F.png")).convert_alpha()
        self.__d_img = image.load(path.join("Frontend\Mania_Window\Img", "D.png")).convert_alpha()
        self.__c_img = image.load(path.join("Frontend\Mania_Window\Img", "C.png")).convert_alpha()
        self.__b_img = image.load(path.join("Frontend\Mania_Window\Img", "B.png")).convert_alpha()
        self.__a_img = image.load(path.join("Frontend\Mania_Window\Img", "A.png")).convert_alpha()
        self.__s_img = image.load(path.join("Frontend\Mania_Window\Img", "S.png")).convert_alpha()
        self.__ss_img = image.load(path.join("Frontend\Mania_Window\Img", "SS.png")).convert_alpha()
        self.__grades = {
            "F": self.__f_img,
            "D": self.__d_img,
            "C": self.__c_img,
            "B": self.__b_img,
            "A": self.__a_img,
            "S": self.__s_img,
            "SS": self.__ss_img
        }

    def show_grade(self, grade: str, screen: Surface):
        self.__check_if_change_current_img(grade=grade)
        screen.blit(self.__current_img, self.__pos.img_coord)

    def __check_if_change_current_img(self, grade: str):
        if self.__current_size == self.__pos.size_tuple[0] and self.__current_grade == grade:
            return
        self.__current_img = transform.scale(self.__grades[grade], self.__pos.size_tuple)
        self.__current_size, self.__current_grade = self.__pos.size_tuple[0], grade


class GradePosSize:
    __SIZE_RATIO = 1.5
    __X_RATIO, __Y_RATIO = 1.76, 7.5

    def __init__(self, pos):
        self.__pos = pos

    @property
    def img_coord(self):
        return self.__x, self.__y

    @property
    def __x(self):
        return self.__pos.width // self.__X_RATIO

    @property
    def __y(self):
        return self.__pos.height // self.__Y_RATIO

    @property
    def size_tuple(self):
        return self.__size, self.__size

    @property
    def __size(self):
        return self.__pos.height // self.__SIZE_RATIO
