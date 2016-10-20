
class NodeTree:
    def __init__(self, data, listCrossComponents = None, parent = None):
        self.data = data # (comp1, comp5): possibility tuple
        self.amount = None
        self.listCrossComponents = listCrossComponents
        self.parent = parent
        self.children = [ ]
        self.isValid = True

    def __repr__(self):
        if self.isValid:
            return str(self.data)
        else:
            return "INVALID"

    def d_print(self):
        """Prints all the details of the NodeTree."""
        print('Node:')
        print(self.data, 'by', self.amount)
        print('Valid: ', self.isValid)
        print('Parent: ', self.parent)
        print('Children: ', self.children)
        print()
    
    def add_child(self, data, listCrossComponents):
        child = NodeTree(data, listCrossComponents, self)
        child.check() # stupid but simpler!
        self.children.append(child)

    def check(self):
        self.determine_amount()
        if self.amount == 0:
            self.isValid = False
            
    def determine_amount(self):
        """Computes the correct value for self.amount"""
        # loop over the components and get the minimum deformable_length
        amount = min(component.deformable_length() for component in self.data)

        #Get the nodes that are leading the deformation
        deformationLeadingNodes = [component.rightNode
                                   for component in self.data]

        # Calculate the deformation that is allowed by the whole deforming
        # cross-components
        amountCrossComponents = cross_components_amount(
            deformationLeadingNodes,
            self.listCrossComponents)
        # ATTENTION! listCrossComponents IS NEEDED!!!
        if amountCrossComponents is not None:
            self.amount = min(amount, amountCrossComponents)
        else:
            self.amount = amount

#########################################################################


def cross_components_amount(deformationLeadingNodes, listCrossComponents):
    """Computes the amount of deformation allowed by the crossComponents"""

    deformingCrossComps = [crossComp for crossComp in listCrossComponents 
                           if crossComp.right_deforms(deformationLeadingNodes)
                           and not 
                           crossComp.left_deforms(deformationLeadingNodes)]

    stretchingCrossComps = [crossComp for crossComp in listCrossComponents 
                            if crossComp.left_deforms(deformationLeadingNodes)
                            and not 
                            crossComp.right_deforms(deformationLeadingNodes)]
    
    if stretchingCrossComps:
        return 0
    
    if deformingCrossComps:
        return min(crossComp.deformable_length()
                   for crossComp in deformingCrossComps)
    
    
    
