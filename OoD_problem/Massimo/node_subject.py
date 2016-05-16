class NodeSubject:
    def __init__(self):
        self.observer_list = [ ]

    def attach(self, observer):
        self.observer_list.append(observer)

    def detach(self, observer):
        self.observer_list.remove(observer)

    def notify(self):
        for observer in self.observer_list:
            observer.update()
        
