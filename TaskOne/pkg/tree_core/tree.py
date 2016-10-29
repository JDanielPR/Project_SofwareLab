from .NodeTree import NodeTree
from ..isdh.isdh_helper import IsdhHelper

class Tree:
    def __init__(self, possibilities, structure):
        self.possibilities = possibilities
        self.root = NodeTree('ROOT')
        self.activeNode = self.root
        self.structure = structure
        self.savers = [ ]
        IsdhHelper().register(self)
        ##
        print('TREE GENERATED')
        self.activeNode.d_print()
        self.print()
        
    def __repr__(self):
        return self.activeNode

    def print(self):
        for key, item in self.savers[0].ood.items():
            print(key)
            for ds in item:
                ds.print()
            print()

    def add_children(self):
        assert not self.activeNode.children
        for data in self.possibilities:
            self.activeNode.add_child(data, self.structure)
        if self.end():
            print('############# ood saved')
            for saver in self.savers:
                saver.save_ood()
        ##
        print('ADDING CHILDREN')
        self.activeNode.d_print()
        self.print()
            
    def end(self):
        if any(node.isValid for node in self.activeNode.children):
            return False # there is at least a valid node
        else:
            # no more valid children the end of the tree has been reached
            return True

    def go_down(self):
        """Changes the activeNode to its first valid child.

If there isn't any valid child, the activeNode is the rightest child and the
tree attribute .end is set to True.
This function should not raise any exception"""
        assert self.activeNode.children
        assert not self.end()
        self.activeNode = self.activeNode.children[0]
##        ##
##        print('GOING DOWN')
##        self.activeNode.d_print()
        self.print()
        if self.activeNode.isValid:
            ##
            print('GONE DOWN')
            self.activeNode.d_print()
            return
        else:
            self.go_right()
        ##
        print('GONE DOWN')
        self.activeNode.d_print()
            
    def go_up(self):
        assert self.activeNode is not self.root
        self.activeNode.isValid = False
        self.undeform()
        self.activeNode = self.activeNode.parent
        ##
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
##        ##
##        print('GOING RIGHT')
##        self.activeNode.d_print()
        self.print()
        if self.activeNode.isValid:
            return
        else:
            self.go_right()

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
