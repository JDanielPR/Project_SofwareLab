import path
class Loadpath(path.Path):
    def __init__(self, integer):
        path.Path.__init__(self)
        self.id = integer
        self.node_list = [ ]
    
    def compute_neighbours(self):
        for member in self.component_list:
            member.add_right_neighbour(self.component_list)
