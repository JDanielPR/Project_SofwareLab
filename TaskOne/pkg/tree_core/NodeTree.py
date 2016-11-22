
class NodeTree:
    def __init__(self, deformingComps, structure = None, parent = None):
        self.amount = None
        self.structure = structure
        self.parent = parent
        self.children = [ ]
        self.isValid = True
        self.keep = None
        self.substitute = False
        
        self.deformingComps = deformingComps # (comp1, comp5):possibility tuple
        self.movingComps = [ ]
        self.deformingCrossComps = [ ]
        self.movingCrossComps = [ ]
        self.stretchingCrossComps = [ ]
        
    def __repr__(self):
        try:
            if self.isValid:
                return str(self.deformingComps)
            else:
                return "INVALID"
        except AttributeError:
            return "NodeTree obj"

    def d_print(self):
        """Prints all the details of the NodeTree."""
        print('Node:')
        print(self.deformingComps, 'by', self.amount)
        print('Valid: ', self.isValid)
        print('Parent: ', self.parent)
        print('Children: ', self.children)
        print()
    
    def add_child(self, deformingComps, structure):
        """Append a child to the list self.children.

        
        If the child is not valid, because the deformingComps contains
        undeformable gaps, other children are created (varying deformingComps)
        and appended to the list self.children.

        Args:
            self:
                the parent NodeTree object
            deformingComps:
                tuple of structure_core.Component objects to deform
            structure:
                the unique structure_core.Structure object, to which
                structure_core.Component objects belong
        Returns:
            nothing is returned
        Raises:
            nothing is raised
        """
        # create the NodeTree object
        child = NodeTree(deformingComps, structure, self)
        # check the amount
        child.check_amount() # child.isValid might be set to False
                             # child.substitute might be set to True
        # initialize a list with the child to append
        next_children = [child]
        # while the child has to be substituted with other children
        while child.substitute:
            # create a new generation of children form the previous one
            next_children = child.next_children(next_children)
                                    # child.substitute might be set to False
        for child in next_children:
            child.check_keep_deforming()
            self.children.append(child)

    def check_amount(self): # here the gap could be substituted
        self.determine_amount()
        if self.amount == 0:
            self.isValid = False
            if any(comp.isGap for comp in self.deformingComps):
                self.substitute = True

    def next_children(self, previous_children = None):
        """"""
        # here self is the child that has to be substituted
        
        # create the list next_deformingComps, with lists of deformingComps
        # for the next generation of children
        next_deformingComps = [ ]
        for child in previous_children:
            for component in child.deformingComps:
                if component.isGap:
                    # create the deformingComps from those of child,
                    # subtituting one gap with the next_gap
                    next_gap = component.next_gap()
                    if next_gap:
                        deformingComps = [comp for comp in child.deformingComps
                                          if comp is not component]
                        deformingComps.append(next_gap)
                        
                        next_deformingComps.append(deformingComps)
                    else:
                        pass
        # if the next_deformingComps list is empty, thus no next generation
        # could be generated
        if not next_deformingComps:
            # stop looking for next generations of children
            self.substitute = False
        # create the next generation of children
        next_children = [ ]
        for deformingComps in next_deformingComps:
            # create child
            child = NodeTree(deformingComps, self.structure)
            # check its amount
            child.check_amount()
            # append it
            next_children.append(child)
        # if there is at least a valid child
        if any(child.isValid for child in next_children):
            # subtitute self in parent.children with next_children
            self.substitute_children(next_children)
            # don't look for next generations of children
            self.substitute = False
        # return the next_generation
        return next_children
    
    def substitute_children(self, next_children):
        """Sets the objects in next_children as proper children of self.parent. 

        Args:
            self:
                the NodeTree object 'child' to substitute, created in
                .add_child()
                REMARK: at this point self.parent exists, but
                self.parent.children doesn't contain self: i.e. the link
                between child and parent only goes from the child to the parent
            next_children:
                list of NodeTree objects to substitute self in the tree.
        Returns:
            Nothing is returned.
        Raises:
            Nothing is raised.
        """

        for child in next_children:
            child.parent = self.parent
            self.parent.children.append(child)
            
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
                                   if comp.deformable_length() > 0
                                   and not comp.isGap]
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
