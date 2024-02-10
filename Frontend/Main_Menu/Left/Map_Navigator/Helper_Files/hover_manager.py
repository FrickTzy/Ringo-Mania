class HoverManager:
    __current_hover_index = None
    __changed = False

    @property
    def changed_hover(self):
        changed = self.__changed
        self.__changed = False
        return changed

    def check_if_change_hover(self, hover_index):
        if self.__current_hover_index == hover_index:
            return
        self.__current_hover_index = hover_index
        self.__changed = True
