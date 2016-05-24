import node
import node_observer as obs

from math import fabs
class Component(obs.NodeObserver):
    def __init__(self, name,
                 node1, node2,
                 deformable_length, deformable_ratio):
        #call base class constructor
        obs.NodeObserver.__init__(self, node1, node2)

        # string type
        self.name = name.strip() # the strip method removes all the whitespaces
        
        # node object at the left end of the component
        self.left_node = node1
        # node object at the right end of the component
        self.right_node = node2

        # length in x direction: computed
        self.length = self.compute_length()

        # deformable length
        self.deformable_length = deformable_length
        # rigid length: computed
        self.rigid_length = self.compute_rigid_length()
        # deformable_ratio
        self.deformable_ratio = deformable_ratio

        # current deformable length
        self.current_deformable_length = deformable_length

    def compute_length(self):
        """It computes the length of the component, as the difference
in x-position between the nodes"""
        return fabs(self.right_node.x_position - self.left_node.x_position)

    def compute_rigid_length(self):
        """It computes the rigid length of the component, as the difference
between length and deformable length"""
        return self.length - self.deformable_length

    def __repr__(self):
        return self.name

    def print_info(self, indentation="", end="\n"):
        """It prints all the information of the component"""
        print(indentation, self.name, ":", sep="")
        print(indentation, "\tleft node at", self.left_node.x_position)
        print(indentation, "\tright node at", self.right_node.x_position)
        print(indentation, "\toverall length of", self.length)
        print(indentation, "\tdeformable length of", self.deformable_length)
        print(indentation, "\trigid length of", self.rigid_length, end)

    def print_current_info(self, indentation="", end="\n"):
        """It prints all the information of the component"""
        print(indentation, self.name, ":", sep="")
        print(indentation, "\tleft node at", self.left_node.current_x)
        print(indentation, "\tright node at", self.right_node.current_x)
        print(indentation, "\toverall length of", self.length)
        print(indentation, "\tdeformable length of", self.current_deformable_length)
        print(indentation, "\trigid length of", self.rigid_length, end)


    def update(self):
        """Updates the current_deformable_length"""
        x2 = self.right_node.current_x
        x1 = self.left_node.current_x
        current_length = x2 - x1
        self.current_deformable_length = current_length - self.rigid_length


    def deform(self, deformation):
        """It deforms the component by moving the right node to the left."""
##        print(self, "has been deformed")
        self.right_node.move_of(deformation)
        try:
            self.right_neighbour.move(deformation)
        except:
            pass

    def move(self, deformation):
##        print(self, "has been moved to the left")
        self.right_node.move_of(deformation)
        try:
            self.right_neighbour.move(deformation)
        except:
            pass

    def virtual_deform(self, infos_collector):
        # check if infos_collector has a max_deformation
        # if not
        if not infos_collector.max_deformation:
            infos_collector.max_deformation = self.current_deformable_length
        # if it already has a max_deformation
        else:
            # check if it is bigger than the current deformable length of this
            # component
            if infos_collector.max_deformation > self.current_deformable_length:
                # if so, update max_deformation with the smaller value
                infos_collector.max_deformation = self.current_deformable_length

        # communicate the virtual deformation to all the observers of the node
        self.right_node.virtual_move(infos_collector)
        try:
            self.right_neighbour.virtual_move(infos_collector)
        except:
            pass

    def virtual_move(self, infos_collector):
        # communicate the virtual deformation to all the observers of the node
        self.right_node.virtual_move(infos_collector)
        try:
            self.right_neighbour.virtual_move(infos_collector)
        except:
            pass

    def say_hi_to(self, infos_collector, node):
        # if it's a member there is nothing to do
        pass                       

    def restore(self):
        self.left_node.restore()
        self.right_node.restore()
        
