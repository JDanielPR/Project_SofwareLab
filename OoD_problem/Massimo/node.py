import node_subject as subj
class Node(subj.NodeSubject):
    def __init__(self, x):
        #call base class constructor
        subj.NodeSubject.__init__(self)

        ######### initial condition
        self.x_position = x

        ######### current condition
        self.current_x = x
        # the current_x is used to simulate deformation, without affecting the
        # inital condition

        # list of the members connected to the left and to the right of the node
        self.left = [ ]
        self.right = [ ]
        
    def restore(self):
        """It restores the initial x position of the node."""
        self.current_x = self.x_position
        self.notify()
        
    def move_of(self, delta_x):
        """It moves the node varying the current_x.
If the current x is 150 and delta_x is 50, then the current x becomes 100."""
        self.current_x -= delta_x
        self.notify()

    def move_to(self, new_x_position):
        pass