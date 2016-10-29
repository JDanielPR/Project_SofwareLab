
class NodeTree:
    def __init__(self, deformingComps, structure = None, parent = None):
        self.amount = None
        self.structure = structure
        self.parent = parent
        self.children = [ ]
        self.isValid = True
        self.keep = None
        
        self.deformingComps = deformingComps # (comp1, comp5):possibility tuple
        self.movingComps = [ ]
        self.deformingCrossComps = [ ]
        self.movingCrossComps = [ ]
        self.stretchingCrossComps = [ ]
        
    def __repr__(self):
        if self.isValid:
            return str(self.deformingComps)
        else:
            return "INVALID"

    def d_print(self):
        """Prints all the details of the NodeTree."""
        print('Node:')
        print(self.deformingComps, 'by', self.amount)
        print('Valid: ', self.isValid)
        print('Parent: ', self.parent)
        print('Children: ', self.children)
        print()
    
    def add_child(self, deformingComps, structure):
        child = NodeTree(deformingComps, structure, self)
        child.check_amount() # stupid but simpler!
        child.check_keep_deforming()
        self.children.append(child)

    def check_amount(self):
        self.determine_amount()
        if self.amount == 0:
            self.isValid = False
            
    def determine_amount(self):
        """Computes the correct value for self.amount"""
        # loop over the components and get the minimum deformable_length
        amount = min(component.deformable_length()
                     for component in self.deformingComps)

        #Get the nodes that are leading the deformation
        deformationLeadingNodes = [component.rightNode
                                   for component in self.deformingComps]

        # Calculate the deformation that is allowed by the deforming
        # cross-components
        amountCrossComponents = self.cross_components_amount(
            deformationLeadingNodes)

        # Get the minimum amount
        if amountCrossComponents is not None:
            self.amount = min(amount, amountCrossComponents)
            # if a connection is limiting the amount of deformation
            if amountCrossComponents < amount:
                self.amount = amountCrossComponents
                # in the next defomation step, every component might deform
                self.keep = False
            # otherwise
            else:
                self.amount = amount
                # the components that are still deformable should keep on
                # deforming
                self.keep = True
        else:
            self.amount = amount
            self.keep = True

    def cross_components_amount(self, deformationLeadingNodes):
        """Computes the amount of deformation allowed by the crossComponents"""

        self.movingComps = [comp
                            for loadpath in self.structure.listLoadpaths
                            for comp in loadpath.listComponents
                            if comp.moves(deformationLeadingNodes)]

        self.deformingCrossComps = [crossComp
                                    for crossComp
                                    in self.structure.listCrossComponents
                                    if crossComp.right_deforms(
                                        deformationLeadingNodes)
                                    and not
                                    crossComp.left_deforms(
                                        deformationLeadingNodes)]

        self.movingCrossComps = [crossComp
                                 for crossComp
                                 in self.structure.listCrossComponents
                                 if crossComp.left_deforms(
                                     deformationLeadingNodes)
                                 and
                                 crossComp.right_deforms(
                                     deformationLeadingNodes)]

        self.stretchingCrossComps = [crossComp
                                     for crossComp
                                     in self.structure.listCrossComponents
                                     if crossComp.left_deforms(
                                         deformationLeadingNodes)
                                     and not
                                     crossComp.right_deforms(
                                         deformationLeadingNodes)]
        
        if self.stretchingCrossComps:
            return 0 # this will result in setting self.isValid = False
        
        if self.deformingCrossComps:
            return min(crossComp.deformable_length()
                       for crossComp in self.deformingCrossComps)

    def check_keep_deforming(self):
        if self.parent.keep:
            # get from the parent node the comps that should keep on deforming
            stillDeformingComps = [comp
                                   for comp in self.parent.deformingComps
                                   if comp.deformable_length() > 0]
            # if one of them is not deforming anymore
            if not all(comp in self.deformingComps
                       for comp in stillDeformingComps):
                # the node is invalid
                self.isValid = False

    def deform(self):
        # deform and move components
        for defComp in self.deformingComps:
            defComp.rightNode.change_position(self.amount)

        for movComp in self.movingComps:
            movComp.rightNode.change_position(self.amount)

        # deformation and movement of crossComponents occur as a consequence

    def undeform(self):
        # deform and move components
        for defComp in self.deformingComps:
            defComp.rightNode.change_position(- self.amount)

        for movComp in self.movingComps:
            movComp.rightNode.change_position(- self.amount)

        # deformation and movement of crossComponents occur as a consequence
