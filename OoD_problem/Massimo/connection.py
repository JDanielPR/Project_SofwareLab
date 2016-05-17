import component as c

class Connection(c.Component):
    def __init__(self, name,
                 node1, node2,
                 deformable_length, deformable_ratio):
        c.Component.__init__(self, name,
                             node1, node2,
                             deformable_length, deformable_ratio)        

