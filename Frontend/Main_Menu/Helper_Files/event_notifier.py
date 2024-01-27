class EventHandlerNotifier:
    __scrolled = False
    __event = None

    @property
    def scrolled(self):
        scrolled = self.__scrolled
        self.__scrolled = False
        return scrolled

    @property
    def event(self):
        return self.__event

    def set_scroll(self):
        self.__scrolled = True

    def set_event(self, event):
        self.__event = event
