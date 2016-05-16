import component as c
class Member(c.Component):
    def __init__(self, name,
                 node1, node2,
                 deformable_length, deformable_ratio):
        c.Component.__init__(self, name,
                             node1, node2,
                             deformable_length, deformable_ratio)

        self.right_neighbour = None

    def add_right_neighbour(self, member_list):
        for member in member_list:
            if self.right_node == member.left_node:
                self.right_neighbour = member
        

