class TimeKeeper:
    def __init__(self, time=None):
        self.time = time

    def set_time(self, time):
        self.time = time

    def get_time(self):
        return self.time