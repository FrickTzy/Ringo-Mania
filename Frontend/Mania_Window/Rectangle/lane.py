from Frontend.Mania_Window.Rectangle.Circles.falling_circles import FallingCircle
from Frontend.Mania_Window.Rectangle.Circles.circles import Circle
from Frontend.Mania_Window.Rectangle.Circles.sliders import Sliders


class Lane:
    def __init__(self, x):
        self.x = x
        self.current_circles: list[FallingCircle] = []
        self.hitting_circle = Circle()
        self.sliders: list[Sliders] = []

    def add_fall_circle(self, window, size):
        self.current_circles.append(FallingCircle(window=window, lane_x=self.x, circle_size=size))

    def add_sliders(self, window, size, min_len):
        self.sliders.append(Sliders(window=window, lane_x=self.x, circle_size=size, min_slider_len=min_len))

    def show_fall_circles(self, height, speed, pause: bool):
        for circles in self.current_circles:
            circles.draw_circles(height=height, speed=speed, pause=pause)

    def show_sliders(self, height, speed, pause: bool):
        for slider in self.sliders:
            slider.draw_slider(height=height, speed=speed, pause=pause)

    def show_hitting_circle(self, window, hitting_circle_y, size) -> None:
        self.hitting_circle.change_size(size=size)
        self.hitting_circle.draw_circles(window=window, x=self.x, y=hitting_circle_y)

    def check_circles_if_out(self):
        for fall_circle in self.current_circles:
            if fall_circle.out:
                self.current_circles.remove(fall_circle)
                return True

    def check_if_end_slider(self):
        for slider in self.sliders:
            if slider.min_slider_len_finished:
                slider.check_if_end_slider()

    def check_circles_if_hit(self, first_hit_window, last_hit_window):
        for circle in self.current_circles:
            if last_hit_window >= circle.hit_box.y > first_hit_window:
                self.current_circles.remove(circle)
                return circle.hit_box.y
        return False

    def check_sliders_if_out(self):
        for slider in self.sliders:
            if slider.out:
                self.sliders.remove(slider)
                return True

    def check_sliders_if_hit(self, first_hit_window, last_hit_window, speed):
        for slider in self.sliders:
            if last_hit_window >= slider.slider_head_hit_box.y > first_hit_window:
                slider.remove_head()
            if last_hit_window >= slider.slider_tail_hit_box.y > first_hit_window + 10:
                slider.remove_tail()
            if slider.get_slider_y() > first_hit_window:
                slider.hold_slider(speed=speed)
        return False

    def check_if_lane_taken(self):
        for slider in self.sliders:
            if not slider.slider_ended:
                return True

    def clear_circles(self) -> None:
        self.current_circles.clear()

    def update_circles(self, size):
        for circle in self.current_circles:
            circle.change_size(size=size)
            circle.update_hit_box(lane_x=self.x, size=size)
        self.hitting_circle.change_size(size=size)
