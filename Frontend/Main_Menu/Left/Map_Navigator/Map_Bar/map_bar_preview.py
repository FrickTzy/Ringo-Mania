from pygame import image, transform
from Backend.Map_Info import MapImage


class MapBarBackgroundPreview:
    __OPACITY = 100

    def __init__(self, pos, image_status):
        name, is_an_anime = image_status
        self.__pos = BackgroundPreviewPos(pos=pos)
        self.__image_checker = MapImage()
        self.__background_image = self.__load_image(title=name, anime_song=is_an_anime)
        self.__final_img = None

    def __load_image(self, title, anime_song):
        return image.load(
            self.__image_checker.get_image(title=title, anime_song=anime_song)).convert_alpha()

    def show_profile(self, main_menu_surface, is_chosen: bool):
        self.__image_setup(chosen=is_chosen)
        img_coord = self.__pos.chosen_img_coord if is_chosen else self.__pos.img_coord
        main_menu_surface.blit(self.__final_img, img_coord)

    def __image_setup(self, chosen: bool = False):
        self.__final_img = transform.scale(self.__background_image, self.__pos.size_tuple)
        self.__set_opacity(chosen=chosen)

    def __set_opacity(self, chosen: bool):
        if chosen:
            self.__final_img.set_alpha(255)
        else:
            self.__final_img.set_alpha(self.__OPACITY)

    @property
    def image(self):
        return self.__background_image


class BackgroundPreviewPos:
    __SIZE_RATIO = 18
    __WIDTH_RATIO, __HEIGHT_RATIO = 5, 1.14
    __X_WIDTH_RATIO = 1.27
    __X_CHOSEN_WIDTH_RATIO = 1.23

    def __init__(self, pos):
        self.__pos = pos

    @property
    def img_coord(self):
        return self.__x, self.y

    @property
    def chosen_img_coord(self):
        return self.__chosen_x, self.y

    @property
    def __x(self):
        return self.__pos.current_map_bar_width - self.__width - 7

    @property
    def __chosen_x(self):
        return self.__pos.current_map_bar_width - self.__width - 7

    @property
    def y(self):
        return self.__pos.record_y + 6

    @property
    def size_tuple(self):
        return self.__width, self.__height

    @property
    def __width(self):
        return self.__pos.record_width // self.__WIDTH_RATIO

    @property
    def __height(self):
        return self.__pos.record_height // self.__HEIGHT_RATIO
