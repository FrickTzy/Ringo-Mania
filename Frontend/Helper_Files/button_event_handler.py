from pygame import mouse


class ButtonEventHandler:
    @classmethod
    def check_buttons_for_clicks(cls, starting_pos: tuple[int, int], size: tuple[int, int], command):
        mouse_pressed = mouse.get_pressed()[0]
        if cls.check_if_mouse_is_in_an_area(starting_pos=starting_pos, size=size) and mouse_pressed:
            command()

    @classmethod
    def check_if_mouse_is_in_an_area(cls, starting_pos: tuple[int, int], size: tuple[int, int]):
        starting_x, starting_y = starting_pos
        ending_x, ending_y = cls.__get_ending_pos(starting_pos, size)
        x, y = mouse.get_pos()
        if starting_x <= x <= ending_x and starting_y <= y <= ending_y:
            return True
        return False

    @classmethod
    def check_if_an_object_is_inside_another_object(cls, starting_pos_1: tuple[int, int], size_1: tuple[int, int],
                                                    starting_pos_2: tuple[int, int], size_2: tuple[int, int]):
        """
        First object is the bigger object and the second object is the smaller one
        :param starting_pos_1:
        :param size_1:
        :param starting_pos_2:
        :param size_2:
        :return bool:
        """

        ending_pos_x_1, ending_pos_y_1 = cls.__get_ending_pos(starting_pos=starting_pos_1, size=size_1)
        ending_pos_x_2, ending_pos_y_2 = cls.__get_ending_pos(starting_pos=starting_pos_2, size=size_2)

        object_2_inside_object_1 = ending_pos_y_1 >= ending_pos_y_2 and ending_pos_x_1 >= ending_pos_x_2

        if not object_2_inside_object_1:
            return False
        if not cls.__check_if_an_object_comes_contact_with_another_object(starting_pos_1=starting_pos_1, size_1=size_1,
                                                                          starting_pos_2=starting_pos_2, size_2=size_2):
            return False

        return True

    @classmethod
    def check_if_an_object_collides_with_another_object(cls, starting_pos_1: tuple[int, int], size_1: tuple[int, int],
                                                        starting_pos_2: tuple[int, int], size_2: tuple[int, int]):
        """
        First object is the bigger object and the second object is the smaller one
        :param starting_pos_1:
        :param size_1:
        :param starting_pos_2:
        :param size_2:
        :return bool:
        """

        ending_pos_x_1, ending_pos_y_1 = cls.__get_ending_pos(starting_pos=starting_pos_1, size=size_1)
        x_2, y_2 = starting_pos_2

        object_2_crosses_object_1 = ending_pos_y_1 >= y_2 and ending_pos_x_1 >= x_2

        if not cls.__check_if_an_object_comes_contact_with_another_object(starting_pos_1=starting_pos_1, size_1=size_1,
                                                                          starting_pos_2=starting_pos_2, size_2=size_2):
            return False
        if not object_2_crosses_object_1:
            return False

        return True

    @classmethod
    def __check_if_an_object_comes_contact_with_another_object(cls, starting_pos_1: tuple[int, int],
                                                               size_1: tuple[int, int],
                                                               starting_pos_2: tuple[int, int],
                                                               size_2: tuple[int, int]):
        """
               First object is the bigger object and the second object is the smaller one
               :param starting_pos_1:
               :param size_1:
               :param starting_pos_2:
               :param size_2:
               :return bool:
               """

        x_1, y_1 = starting_pos_1
        x_2, y_2 = starting_pos_2

        ending_pos_x_1, ending_pos_y_1 = cls.__get_ending_pos(starting_pos=starting_pos_1, size=size_1)
        ending_pos_x_2, ending_pos_y_2 = cls.__get_ending_pos(starting_pos=starting_pos_2, size=size_2)

        second_object_x_inside_first_object_x = x_1 <= x_2
        second_object_x_inside_first_object_ending_x = x_2 <= ending_pos_x_1

        second_object_y_inside_first_object_y = y_1 <= y_2
        second_object_y_inside_first_object_ending_y = y_2 <= ending_pos_y_2

        if not second_object_x_inside_first_object_x:
            return False
        elif not second_object_x_inside_first_object_ending_x:
            return False
        elif not second_object_y_inside_first_object_y:
            return False
        elif not second_object_y_inside_first_object_ending_y:
            return False
        return True

    @staticmethod
    def __get_ending_pos(starting_pos: tuple[int, int], size: tuple[int, int]) -> tuple[int, int]:
        starting_x, starting_y = starting_pos
        width, height = size
        return starting_x + width, starting_y + height
