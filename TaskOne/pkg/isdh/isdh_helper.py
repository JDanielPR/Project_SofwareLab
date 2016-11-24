import pkg
from .component import Component
from .deformation_step import DeformationStep

class IsdhHelper:
    def __init__(self):
        self.i_s = [ ] # initial state list
        self.d_h = [ ] # deformation history list (list of dictionaries)
        self.isdh_dict = dict() # isdh_dict[comp] == isdh_comp
        self.ood = dict()
        self.amount = 0

    def register(self, tree):
        """Register the saver to tree.

        Append self to tree.savers, initialise self.i_s, initialise self.ood.

        Args:
            tree:
                a tree_core.tree.Tree object
        Returns:
            nothing is returned
        Raises:
            nothing is raised
        """
        assert type(tree) is pkg.tree_core.tree.Tree
        
        ## register the IsdhHelper
        tree.savers.append(self)

        ## initialise self.i_s
        # create a list with all the components to save (ignore gaps)
        components = [comp for loadpath in tree.structure.listLoadpaths
                      for comp in loadpath.listComponents
                      if not comp.isGap]
        # create a list with all the crossComponents
        crossComps = [crossComp
                      for crossComp in tree.structure.listCrossComponents]
        # loop over components
        for comp in components:
            # for each component
            # create an isdh.Component
            isdh_comp = Component(comp.name,
                                  comp.leftNode.position,
                                  comp.rightNode.position,
                                  comp.length() - comp.rigidLength,
                                  comp.leftNode.loadpathLevel,
                                  comp.rightNode.loadpathLevel)
            # save it in the initial state list
            self.i_s.append(isdh_comp)
            # save the link: Component -> isdh.Component
            self.isdh_dict[comp] = isdh_comp
        # loop over crossComponents
        for comp in crossComps:
            # for each crossComponent
            # create an isdh.Component
            isdh_comp = Component(comp.name,
                                  comp.leftNode.position,
                                  comp.rightNode.position,
                                  comp.length() - comp.rigidLength,
                                  comp.leftNode.loadpathLevel,
                                  comp.rightNode.loadpathLevel)
            # save it in the initial state list
            self.i_s.append(isdh_comp)
            # save the link: crossComponent -> isdh.Component
            self.isdh_dict[comp] = isdh_comp

        ## initialise self.ood
        self.init_ood()

    def save(self, activeNode):
        """Save a defromation step of the whole structure.

        Args:
            activeNode:
                a tree_core.node_tree.NodeTree object
        Returns:
            nothing is returned
        Raises:
            nothing is raised
        """
        
        # save the deformation step for:
        # - deforming components
        for defComp in activeNode.deformingComps:
            self.save_defo_step(defComp, 'd', activeNode.amount)

        # - moving components
        for movComp in activeNode.movingComps:
            self.save_defo_step(movComp, 'm', activeNode.amount)
                
        # - deforming crossComponents
        for defCrossComp in activeNode.deformingCrossComps:
            self.save_defo_step(defCrossComp, 'd', activeNode.amount)
                
        # - moving crossComponents
        for movCrossComp in activeNode.movingCrossComps:
            self.save_defo_step(movCrossComp, 'm', activeNode.amount)

        # update the amount of deformation that the structure underwent so far
        self.update_amount(activeNode.amount)
            
    def unsave(self, activeNode):
        """Un-save a defromation step of the whole structure.

        Args:
            activeNode:
                a tree_core.node_tree.NodeTree object
        Returns:
            nothing is returned
        Raises:
            nothing is raised
        """
        # update the amount of deformation that the structure underwent so far
        self.update_amount(- activeNode.amount)

        # unsave the deformation step for:
        # - deforming components
        for defComp in activeNode.deformingComps:
            self.save_defo_step(defComp, 'd', - activeNode.amount)

        # - moving components
        for movComp in activeNode.movingComps:
            self.save_defo_step(movComp, 'm', - activeNode.amount)
                
        # - deforming crossComponents
        for defCrossComp in activeNode.deformingCrossComps:
            self.save_defo_step(defCrossComp, 'd', - activeNode.amount)
                
        # - moving crossComponents
        for movCrossComp in activeNode.movingCrossComps:
            self.save_defo_step(movCrossComp, 'm', - activeNode.amount)

    def save_defo_step(self, comp, stepType, stepAmount):
        """Save or un-save a deformation step of one component.

        Args:
            comp:
                a structure_core.component.Component object
                or
                a structure_core.cross_component.CrossComponent object
            stepType:
                'd' or 'm' (deformation or movement)
            stepAmount:
                a double, the amount of deformation of the step
        Returns:
            nothing is returned
        Raises:
            nothing is raised
        """
        # ignore gaps
        try:
            if comp.isGap:
                return 
        except AttributeError:
            pass # comp is a connection, ignore exception
        
        assert self.isdh_dict[comp] in self.i_s
        assert stepType in ['d', 'm']

        # get the related isdh_comp
        isdh_comp = self.isdh_dict[comp]

        if stepAmount > 0:
            # save the new deformation step
            step = DeformationStep(stepAmount, self.amount, stepType)
            self.ood[isdh_comp].append(step)

        elif stepAmount < 0:
            # unsave the old deformation step
            assert self.ood[isdh_comp][-1] == DeformationStep(-stepAmount,
                                                              self.amount,
                                                              stepType)
            step = self.ood[isdh_comp].pop()

        assert stepAmount != 0

    def update_amount(self, amount):
        """Update the amount of deformation occured so far.

        Args:
            amount:
                a double, the amount of deformation of the new deformation
                step.
        Returns:
            nothing is returned
        Raises:
            nothing is raised
        """
        self.amount += amount

    def init_ood(self):
        """Initialise self.ood.

        Args:
            nothing is taken
        Returns:
            nothing is returned
        Raises:
            nothing is raised
        """
        # initialise the dictionary with the elements of self.i_s as keys
        # and an empty list as value
        for isdh_comp in self.i_s:
            self.ood[isdh_comp] = [ ]

    def copy_ood(self):
        """Return a copy of self.ood, with original key and a copy of value.

        The copy returned is a dictionary, in which the keys are references to
        the original keys, and the values are copies.
        This way the items in self.i_s can be used as keys for the copy and,
        at the same time, modifications to self.ood do not modify the copy.

        Args:
            nothing is taken.
        Returns:
            a dictionary is returned.
        Raises:
            nothing is raised.
        """        
        copy = dict()
        for key, value in self.ood.items():
            copy[key] = value.copy()
        return copy 

    def save_ood(self):
        """Save the Order of Deformation in self.ood as a solution.

        Args:
            nothing is taken.
        Returns:
            nothing is returned.
        Raises:
            nothing is raised.
        """
        self.d_h.append(self.copy_ood())
        
