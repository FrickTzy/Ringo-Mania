import pygame
from Stuff.Ringo_Mania.Frontend.settings import FPS, COMBO_X, SCORE_Y, BLACK, clock, \
    PURPLE, END_SONG_DELAY, MID_COMBO_X, MID_COMBO_Y, RECT_COMBO_DISPLAY, \
    RECORD_X
from Stuff.Ringo_Mania.Frontend.main_rectangle import Rectangle
from Stuff.Ringo_Mania.Frontend.records import Record
from Stuff.Ringo_Mania.Frontend.font import Font
from Stuff.Ringo_Mania.Frontend.display import Display
from Stuff.Ringo_Mania.Frontend.combo import ComboCounter


class PlayWindow:
    running = False

    def __init__(self, music, timer, map_manager, play_tracker, song="Bocchi"):
        self.display: Display = Display()
        self.font = Font()
        self.record = Record(self.font)
        self.music = music
        self.play_tracker = play_tracker
        self.music.set_music(song)
        self.timer = timer
        self.map_manager = map_manager(song)
        self.combo_counter = ComboCounter(self.font)
        self.rectangle = Rectangle(window=self.display.window, music=self.music, maps=self.map_manager,
                                   timer=self.timer,
                                   display=self.display, combo_counter=self.combo_counter)

    def run(self):
        self.background_setup()
        while self.running:
            self.timer.compute_time()
            self.update_frame()
            self.rectangle.run()
            self.show_record()
            self.show_combo_and_life()
            self.check_events()
        pygame.quit()

    def show_combo_and_life(self):
        combo, mid_combo, score, acc, life = self.combo_counter.show_combo()
        self.combo_counter.update_life_bar_coord(self.display.life_bar_coordinates)
        life_bar_height = self.combo_counter.get_life_bar_height()
        self.show_life_bar(life_bar_height)
        self.display.window.blit(combo, (COMBO_X, self.display.combo_pos_y))
        self.display.window.blit(score, (self.display.score_pos_x, SCORE_Y))
        self.display.window.blit(acc, (self.display.acc_pos_x, self.display.acc_y))
        if RECT_COMBO_DISPLAY:
            self.display.window.blit(mid_combo, (MID_COMBO_X, MID_COMBO_Y))

    def show_record(self):
        self.font.update_all_font(self.display.height)
        for index, record in enumerate(self.record.show_record(self.rectangle.combo_counter.info)):
            score, combo, name = record
            self.display.window.blit(score,
                                     (RECORD_X, self.display.record_y + (index * self.display.record_y_interval)))
            self.display.window.blit(combo, (RECORD_X + self.display.score_padding,
                                             self.display.record_y + (index * self.display.record_y_interval)))
            self.display.window.blit(name, (RECORD_X, self.display.name_y + (index * self.display.record_y_interval)))

    def show_life_bar(self, coord):
        pygame.draw.rect(self.display.window, PURPLE, self.display.life_bar_coordinates)
        pygame.draw.rect(self.display.window, BLACK, coord)

    def background_setup(self):
        music_length = self.music.play_music()
        self.running = True
        self.rectangle.init_circles()
        self.timer.update_target_time(music_length, END_SONG_DELAY)
        self.record.init_record(self.play_tracker.check_plays())

    def update_frame(self):
        clock.tick(FPS)
        pygame.display.update()
        self.display.window.fill(BLACK)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        if self.rectangle.combo_counter.life == 0:
            self.rectangle.failed = True
        if self.timer.timer_finished or self.rectangle.map_finished:
            self.rectangle.map_finished = True
            self.play_tracker.update_plays(self.rectangle.combo_counter.get_stats())

        # self.window.get_size()


if __name__ == "__main__":
    window = PlayWindow("", "")
    window.run()
