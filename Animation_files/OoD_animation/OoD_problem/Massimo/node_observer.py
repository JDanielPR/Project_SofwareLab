class NodeObserver:
    def __init__(self, node1, node2):
        node1.attach(self)
        node2.attach(self)

    def update(self):
        raise NotImplementedError("Subclass must implement abstract method")        
