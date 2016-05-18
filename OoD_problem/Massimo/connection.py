import component as c

class Connection(c.Component):
    def __init__(self, name,
                 node1, node2,
                 deformable_length, deformable_ratio):
        c.Component.__init__(self, name,
                             node1, node2,
                             deformable_length, deformable_ratio)
        self.previous_deformable_length = deformable_length

    def restore(self):
        self.left_node.restore()
        self.right_node.restore()
        self.previous_deformable_length = self.current_deformable_length
