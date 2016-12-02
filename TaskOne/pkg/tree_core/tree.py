from .node_tree import NodeTree
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
            string
        Raises:
            nothing is raised
        """
        try:
            return self.activeNode.__repr__()
        except AttributeError:
            return "Tree obj"

    def print(self):
        """Print in detail the current Order of Deformation, as saved.

        The dictionary self.savers[0].ood contains, for each component, the
        list of isdh.DeformationStep objects from the tree root to
        self.activeNode.
        self.savers[0].ood = {  isdh-comp1 : [DeformationStep1,
                                              DeformationStep2,
                                              ...],
                                isdh-comp2 : [DeformationStep1,
                                              DeformationStep2,
                                              ...],
                                isdh-comp3 : [DeformationStep1,
                                              DeformationStep2,
                                              ...],
                              }
        The content of this dictionary is printed in detail.
        
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
        """Add children to self.activeNode.

        The children of self.activeNode are generated and appended to the list
        self.activeNode.children.
        If the end of the tree as been reached (no valid child has been found),
        the current Order of Deformation is saved.

        Args:
            nothing is taken
        Returns:
            nothing is returned
        Raises:
            nothing is raised
        """
        assert not self.activeNode.children
        self.structure.reset_connections_to_barrier_and_firewall()
        for data in self.structure.get_deforming_components():
            self.activeNode.add_child(data, self.structure)
        # if it isn't possible to keep deforming, activate the children with a
        # positive amount
        if self.end():
            for node in self.activeNode.children:
                if node.amount > 0:
                    node.isValid = True
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
            nothing is taken
        Returns:
            True if self.activeNode has any valid children,
            False otherwise
        Raises:
            Nothing is raised
        """
        
        if any(node.isValid for node in self.activeNode.children):
            return False # there is at least a valid node
        else:
            # no more valid children the end of the tree has been reached
            return True

    def go_down(self):
        """Changes the activeNode to its first valid child.

        If there isn't any valid child, the activeNode is the rightest child 
        and the function raises a StopIteration error.

        Args:
            nothing is taken
        Returns:
            nothing is returned
        Raises:
            StopIteration
        """
        StopIteration
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
        """Changes the activeNode to its parent.

        The parent becomes the activeNode and the structure is consistently
        undeformed restoring the state before the deformation of self.

        Args:
            nothing is taken
        Returns:
            nothing is returned
        Raises:
            Nothing is raised
        """
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

        If the neighbour doesn't exist, a StopIteration exception is raised.

        Args:
            nothing is taken
        Returns:
            nothing is returned
        Raises:
            StopIteration       
        """ 
        
        children = iter(self.activeNode.parent.children)
        for child in children:
            if child == self.activeNode:
                child = next(children)
                break
        self.activeNode = child
        while not self.activeNode.isValid:
            self.activeNode = next(children)

    def deform(self):
        """Deforms the structure according to the active node.

        The deformationSteps that occur as a consequence are saved by the
        savers.
        
        Args:
            nothing is taken
        Returns:
            nothing is returned
        Raises:
            nothing is raised
        """
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
        """Undeforms the structure according to the active node.

        The deformationSteps that are undone as a consequence are unsaved by
        the savers.
        
        Args:
            nothing is taken
        Returns:
            nothing is returned
        Raises:
            nothing is raised
        """
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

        It surfs the tree going down or right according to the blackbox
        response.

        Args:
            blackbox:
                a function that decides whether self.activeNode is the valid
                next deformationStep or not.
        Returns:
            True, if self.activeNode or one of its neighbours was the correct
            one.
            False, if neither self.activeNode nor one of its neighbours was the
            correct one.
        Raises:
            exceptions raised by the blackbox, remain unhandled.
        """
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
