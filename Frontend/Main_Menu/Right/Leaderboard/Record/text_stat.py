from pygame import font
from Frontend.Settings import Color, PLAYER_NAME


class TextStats:
    __COLOR = Color.WHITE

    def __init__(self, play_info, pos):
        self.__font = Font()
        self.__pos = TextPos(pos=pos)
        self.__play_info: dict = play_info

    def show_text(self, main_menu_surface):
        self.__font.check_if_change_font(height=self.__pos.height)
        player_name = self.__font.font.render(PLAYER_NAME, True, self.__COLOR)
        score = self.__font.font.render(f"{self.__play_info['score']}", True, self.__COLOR)
        accuracy = self.__font.font.render(
            f"{format(float(str(self.__play_info['accuracy']).removesuffix('%')), '.2f')}%",
            True, self.__COLOR)
        main_menu_surface.blit(player_name, self.__pos.name_pos())
        main_menu_surface.blit(score, self.__pos.score_pos())
        main_menu_surface.blit(accuracy, self.__pos.acc_pos())

    def show_static_text(self, main_menu_surface, y):
        self.__font.check_if_change_font(height=self.__pos.height)
        player_name = self.__font.font.render(PLAYER_NAME, True, self.__COLOR)
        score = self.__font.font.render(str(self.__play_info["score"]), True, self.__COLOR)
        accuracy = self.__font.font.render(str(self.__play_info["accuracy"]), True,
                                           self.__COLOR)
        main_menu_surface.blit(player_name, self.__pos.name_pos(y=y))
        main_menu_surface.blit(score, self.__pos.score_pos(y=y))
        main_menu_surface.blit(accuracy, self.__pos.acc_pos(y=y))


class Font:
    __FONT_RATIO = 50
    __current_height = 0

    def __init__(self):
        self.__font = font.SysFont("arialblack", 30)

    @property
    def font(self):
        return self.__font

    def __set_font(self, height):
        self.__font = font.SysFont("arialblack", self.__font_size(height=height))

    def check_if_change_font(self, height):
        if self.__current_height == height:
            return
        self.__set_font(height=height)
        self.__current_height = height

    def __font_size(self, height):
        return int(height // self.__FONT_RATIO)

    def text_size(self, text: str) -> tuple[int, int]:
        width, height = self.__font.size(text)
        return width, height


class TextPos:
    __X_RATIO = 1.89
    __SONG_NAME_RATIO, __SONG_ARTIST_RATIO = 40, 11.43

    def __init__(self, pos):
        self.__pos = pos

    @property
    def height(self):
        return self.__pos.height

    def name_pos(self, y=0):
        if not y:
            pos = self.__pos.record_x + 100, self.__pos.record_y + 5
        else:
            pos = self.__pos.record_x + 100, y + 5
        return pos

    def score_pos(self, y=0):
        if not y:
            pos = self.__pos.record_x + 450, self.__pos.record_y + 5
        else:
            pos = self.__pos.record_x + 450, y + 5
        return pos

    def acc_pos(self, y=0):
        if not y:
            pos = self.__pos.record_x + 450, self.__pos.record_y + 25
        else:
            pos = self.__pos.record_x + 450, y + 25
        return pos
