from .NodeTree import NodeTree
from ..isdh.isdh_helper import IsdhHelper
PRINT = False
class Tree:
    def __init__(self, structure):
        """Constructor of the class tree_core.Tree.

        Args:
            structure:
                the structure_core.Structure object to which the tree is linked
        Returns:
            nothing is returned
        Raises:
            nothing is raised
        """
        self.root = NodeTree('ROOT')
        self.activeNode = self.root
        self.structure = structure
        self.savers = [ ]
        IsdhHelper().register(self)
        ##
        if PRINT:
            print('TREE GENERATED')
            self.activeNode.d_print()
            self.print()
        
    def __repr__(self):
        """Return the string representation of the object.

        If the activeNode attribute is defined, its string representation is
        returned. Otherwise "Tree obj" is returned.
        
        Args:
            nothing is taken
        Returns:
            nothing is returned
        Raises:
            nothing is raised
"""
        try:
            return self.activeNode.__repr__()
        except AttributeError:
            return "Tree obj"

    def print(self):
        """Print in detail the current Order of Deformation, as saved.

        The content of 
        
        Args:
            nothing is taken
        Returns:
            nothing is returned
        Raises:
            nothing is raised
"""
        for key, item in self.savers[0].ood.items():
            print(key)
            for ds in item:
                ds.print()
            print()

    def add_children(self):
        """Add children to self.activeNode."""
        assert not self.activeNode.children
        self.structure.reset_connections_to_barrier_and_firewall()
        for data in self.structure.get_deforming_components():
            self.activeNode.add_child(data, self.structure)
################################ UNDER TESTING ################################ 
        # if it isn't possible to keep deforming, activate the children with a
        # positive amount
        if self.end():
            for node in self.activeNode.children:
                if node.amount > 0:
                    node.isValid = True
################################ UNDER TESTING ################################                     
        if self.end():
            for saver in self.savers:
                saver.save_ood()
            if PRINT: ##
                print('############# ood saved')
        ##
        if PRINT:
            print('ADDING CHILDREN')
            self.activeNode.d_print()
        
    def end(self):
        """end() -> True or False.

        Args:
            self:
        Returns:
            True if self.activeNode has any valid children,
            False otherwise.
        Raises:
        """
        
        if any(node.isValid for node in self.activeNode.children):
            return False # there is at least a valid node
        else:
            # no more valid children the end of the tree has been reached
            return True

    def go_down(self):
        """Changes the activeNode to its first valid child.

        If there isn't any valid child, the activeNode is the rightest child.
        This function should not raise any exception.
        """
        assert self.activeNode.children
        assert not self.end()
        self.activeNode = self.activeNode.children[0]
        if self.activeNode.isValid:
            ##
            if PRINT:
                print('GONE DOWN')
                self.activeNode.d_print()
            return
        else:
            self.go_right()
        ##
        if PRINT:
            print('GONE DOWN')
            self.activeNode.d_print()
            
    def go_up(self):
        assert self.activeNode is not self.root
        self.activeNode.isValid = False
        self.undeform()
        self.activeNode = self.activeNode.parent
        self.structure.reset_connections_to_barrier_and_firewall()
        ##
        if PRINT:
            self.activeNode.d_print()

    def go_right(self):
        """Changes the activeNode to its right neighbour.

If the neighbour doesn't exist, a StopIteration exception is raised.""" 
        
        children = iter(self.activeNode.parent.children)
        for child in children:
            if child == self.activeNode:
                child = next(children)
                break
        self.activeNode = child
        while not self.activeNode.isValid:
            self.activeNode = next(children)

    def deform(self):
        """Deforms the structure according to the active node"""
        # if self.activeNode is the ROOT, just pass
        if self.activeNode is self.root:
            return
        # deform the structure
        self.activeNode.deform()
        # save deformation steps
        for saver in self.savers:
            saver.save(self.activeNode)
        if PRINT:
            self.print()

    def undeform(self):
        """Undeforms the structure according to the active node"""
        # if self.activeNode is the ROOT, just pass
        if self.activeNode is self.root:
            return
        # unsave deformation steps
        for saver in self.savers:
            saver.unsave(self.activeNode)
        # undeform the structure
        self.activeNode.undeform()

    def surf(self, blackbox):
        """Changes the activeNode.

It goes down or right according to the blackbox response."""
        assert self.activeNode.isValid

        activeNodeIsCorrect = blackbox(self)
        # if the blackbox can't decide, it should raise an exeption, that will
        # remain unhandled.
        # so the possible answers are:
        # 1. return True
        # 2. return False
        # 3. raise ImpossibleDecision (e.g.)

        if activeNodeIsCorrect:
            self.deform()
            self.add_children()
            if not self.end():
                self.go_down()          
        else:
            try:
                self.go_right()
            except StopIteration:
                return False # no more right neighbours
        return True
