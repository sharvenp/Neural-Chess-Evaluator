class Observable:

    def __init__(self):
        self._observers = []

    def add_observer(self, o):
        self._observers.append(o)

    def notify_all(self):
        for o in self._observers:
            o.update(self)
