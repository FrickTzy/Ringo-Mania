from pygame import mouse


class ButtonEventHandler:
    @classmethod
    def check_buttons_for_clicks(cls, starting_pos: tuple[int, int], size: tuple[int, int], command):
        starting_x, starting_y = starting_pos
        ending_x, ending_y = cls.__get_ending_pos(starting_pos, size)
        x, y = mouse.get_pos()
        if (starting_x <= x <= ending_x and starting_y <= y <= ending_y) and mouse.get_pressed()[0]:
            command()

    @classmethod
    def check_if_mouse_is_in_an_area(cls, starting_pos: tuple[int, int], size: tuple[int, int]):
        starting_x, starting_y = starting_pos
        ending_x, ending_y = cls.__get_ending_pos(starting_pos, size)
        x, y = mouse.get_pos()
        if starting_x <= x <= ending_x and starting_y <= y <= ending_y:
            return True
        return False

    @staticmethod
    def __get_ending_pos(starting_pos: tuple[int, int], size: tuple[int, int]) -> tuple[int, int]:
        starting_x, starting_y = starting_pos
        width, height = size
        return starting_x + width, starting_y + height
