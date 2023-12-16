from pygame import mouse


class ButtonEventHandler:
    @classmethod
    def check_buttons_for_clicks(cls, starting_pos: tuple[int, int], text_size: tuple[int, int], command):
        starting_x, starting_y = starting_pos
        ending_x, ending_y = cls.__get_ending_pos(starting_pos, text_size)
        x, y = mouse.get_pos()
        if (starting_x <= x <= ending_x and starting_y <= y <= ending_y) and mouse.get_pressed()[0]:
            command()

    @staticmethod
    def __get_ending_pos(starting_pos: tuple[int, int], text_size: tuple[int, int]) -> tuple[int, int]:
        starting_x, starting_y = starting_pos
        text_width, text_height = text_size
        return starting_x + text_width, starting_y + text_height
