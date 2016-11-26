import path
class Loadpath(path.Path):
    def __init__(self, integer):
        path.Path.__init__(self)
        self.id = integer
        self.node_list = [ ]
