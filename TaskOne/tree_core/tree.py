from .NodeTree import NodeTree

class Tree:
    def __init__(self, possibilities, listCrossComponents):
        self.possibilities = possibilities
        self.root = NodeTree('ROOT')
        self.activeNode = self.root
        self.end = False
        self.listCrossComponents = listCrossComponents
        ##
        print('TREE GENERATED')
        self.activeNode.d_print()
        
    def __repr__(self):
        return self.activeNode

    def add_children(self):
        assert not self.activeNode.children
        for data in self.possibilities:
            self.activeNode.add_child(data, self.listCrossComponents)
        if any(node.isValid for node in self.activeNode.children):
            pass # there is at least a valid node
        else:
            # no more valid children the end of the tree has been reached
            self.end = True
        ##
        print('ADDING CHILDREN')
        self.activeNode.d_print()

    def go_down(self):
        """Changes the activeNode to its first valid child.

If there isn't any valid child, the activeNode is the rightest child and the
tree attribute .end is set to True.
This function should not raise any exception"""
        assert self.activeNode.children
        assert not self.end
        self.activeNode = self.activeNode.children[0]
        ##
        print('GOING DOWN')
        self.activeNode.d_print()
        if self.activeNode.isValid:
            return
        else:
            self.go_right()
            
    def go_up(self):
        self.end = False # carefully think about that!
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
        ##
        print('GOING RIGHT')
        self.activeNode.d_print()
        if self.activeNode.isValid:
            return
        else:
            self.go_right()

    def deform(self):
        """Deforms the structure according to the active node"""
        # if self.activeNode is the ROOT, just pass
        if self.activeNode is self.root:
            return
        # for each component in data deform
        amount = self.activeNode.amount
        for component in self.activeNode.data:
            component.deform(amount)

    def undeform(self):
        """Undeforms the structure according to the active node"""
        # if self.activeNode is the ROOT, just pass
        if self.activeNode is self.root:
            return
        # for each component in data deform
        amount = self.activeNode.parent.amount
        for component in self.activeNode.parent.data:
            component.deform(-amount) # mind the minus, here we UN-deform

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
            if not self.end:
                self.go_down()          
        else:
            try:
                self.go_right()
            except StopIteration:
                return False # no more right neighbours
        return True
