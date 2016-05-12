class Member:
    def __init__(self, left_node, right_node):
        # node object at the left end of the member
        self.left_node = left_node
        
        # node object at the right end of the member
        self.right_node = right_node

        # length in x direction
        self.length = self.compute_length()

        self.starting_loadpath = None

    def compute_length(self):
        """"It computes the length of the member, as the difference
in x-position between the nodes"""
        self.length = self.right_node.x_position - self.left_node.y_position
