import node
from math import fabs
class Component:
    def __init__(self, name,
                 node1, node2,
                 deformable_length, deformable_ratio):
        # string type
        self.name = name.strip() # the strip method removes all the whitespaces
        
        # node object at the left end of the component
        self.left_node = node1
        # node object at the right end of the component
        self.right_node = node2

        # length in x direction: computed
        self.length = self.compute_length()

        #
        self.starting_loadpath = None
        self.ending_loadpath = None

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

    def deform(self, partial_deformation = False):
        """It deforms the component by changing current_deformable_length and
current_x of the right node."""
        if partial_deformation:
            # deform partially the component, after checking if the deformation
            # makes sense
            if partial_deformation < self.current_deformable_length:
                self.right_node.move(partial_deformation)
                self.current_deformable_length -= partial_deformation
            else:
                print("Something wrong is passing: deforming ",
                      self.name, "of", partial_deformation)
        else:
            # get the remaining deformable length and deform the component
            # completely, moving the right node to the right
            self.right_node.move(self.current_deformable_length)
            self.current_deformable_length = 0

    def move(self, delta_x):
        """It moves the component to the left."""
        self.left_node.move(delta_x)
        self.right_node.move(delta_x)


    def print_info(self, indentation="", end="\n"):
        """It prints all the information of the component"""
        print(indentation, self.name, ":", sep="")
        print(indentation, "\tleft node at", self.left_node.x_position)
        print(indentation, "\tright node at", self.right_node.x_position)
        print(indentation, "\toverall length of", self.length)
        print(indentation, "\tdeformable length of", self.deformable_length)
        print(indentation, "\trigid length of", self.rigid_length, end)
