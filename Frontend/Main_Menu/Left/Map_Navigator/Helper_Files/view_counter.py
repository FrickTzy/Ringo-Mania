class ViewCounter:
    MAX_BAR_VIEW = 8
    MAX_BAR_SCROLL = 4
    current_map_bar_view = 0
    current_top_view = 0
    filtered_top_view = 0

    def reset_view(self):
        self.current_map_bar_view = 0

    def check_if_viewed(self, map_bar):
        if map_bar.is_viewed:
            self.current_map_bar_view += 1

    def reset_filtered_view(self):
        self.filtered_top_view = 0
