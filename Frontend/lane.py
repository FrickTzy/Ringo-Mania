from Stuff.Ringo_Mania.Frontend.falling_circles import FallingCircle
from Stuff.Ringo_Mania.Frontend.circles import Circle


class Lane:
    def __init__(self, x):
        self.x = x
        self.current_circles: list[FallingCircle] = []
        self.hitting_circle = Circle()

    def add_fall_circle(self, window, size):
        self.current_circles.append(FallingCircle(window=window, lane_x=self.x, circle_size=size))

    def show_fall_circles(self, height, speed, pause: bool):
        for circles in self.current_circles:
            circles.draw_circles(height=height, speed=self.lane_circle_manager.circle_speed, pause=pause)

    def show_hitting_circle(self, window, hitting_circle_y, size) -> None:
        self.hitting_circle.change_size(size=size)
        self.hitting_circle.draw_circles(window=window, x=self.x, y=hitting_circle_y)

    def check_circles_if_out(self):
        for fall_circle in self.current_circles:
            if fall_circle.out:
                self.current_circles.remove(fall_circle)
                return True

    def check_circles_if_hit(self, first_hit_window, last_hit_window):
        for circle in self.current_circles:
            if last_hit_window >= circle.hit_box.y > first_hit_window:
                self.current_circles.remove(circle)
                return True
        return False
