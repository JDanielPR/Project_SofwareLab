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
        """Append self to tree.savers and initialise self.i_s."""
        print(type(tree))
        assert type(tree) is pkg.tree_core.tree.Tree
        # register the IsdhHelper
        tree.savers.append(self)
        # initialise self.i_s
        components = [comp for loadpath in tree.structure.listLoadpaths
                      for comp in loadpath.listComponents
                      if not comp.isGap]
        crossComps = [crossComp
                      for crossComp in tree.structure.listCrossComponents]
        for comp in components:
            isdh_comp = Component(comp.name,
                                  comp.leftNode.position,
                                  comp.rightNode.position,
                                  comp.length() - comp.rigidLength,
                                  comp.leftNode.loadpathLevel,
                                  comp.rightNode.loadpathLevel)
            self.i_s.append(isdh_comp)
            self.isdh_dict[comp] = isdh_comp
        for comp in crossComps:
            isdh_comp = Component(comp.name,
                                  comp.leftNode.position,
                                  comp.rightNode.position,
                                  comp.length() - comp.rigidLength,
                                  comp.leftNode.loadpathLevel,
                                  comp.rightNode.loadpathLevel)
            self.i_s.append(isdh_comp)
            self.isdh_dict[comp] = isdh_comp
            
        self.init_ood()

    def save(self, activeNode):
        """Save a defromation step of the whole structure."""

        for defComp in activeNode.deformingComps:
            self.save_defo_step(defComp, 'd', activeNode.amount)

        for movComp in activeNode.movingComps:
            self.save_defo_step(movComp, 'm', activeNode.amount)
                
        for defCrossComp in activeNode.deformingCrossComps:
            self.save_defo_step(defCrossComp, 'd', activeNode.amount)
                
        for movCrossComp in activeNode.movingCrossComps:
            self.save_defo_step(movCrossComp, 'm', activeNode.amount)

        self.update_amount(activeNode.amount)
            
    def unsave(self, activeNode):
        """Un-save a defromation step of the whole structure."""

        self.update_amount(- activeNode.amount)

        for defComp in activeNode.deformingComps:
            self.save_defo_step(defComp, 'd', - activeNode.amount)

        for movComp in activeNode.movingComps:
            self.save_defo_step(movComp, 'm', - activeNode.amount)
                
        for defCrossComp in activeNode.deformingCrossComps:
            self.save_defo_step(defCrossComp, 'd', - activeNode.amount)
                
        for movCrossComp in activeNode.movingCrossComps:
            self.save_defo_step(movCrossComp, 'm', - activeNode.amount)

    def save_defo_step(self, comp, stepType, stepAmount):
        """Save or un-save a deformation step of one component."""

        try:
            if comp.isGap:
                return
        except AttributeError:
            pass
        assert self.isdh_dict[comp] in self.i_s
        assert stepType in ['d', 'm']
        # get the related isdh_comp
        isdh_comp = self.isdh_dict[comp]

        if stepAmount > 0:
            # save the new deformation step
            step = DeformationStep(stepAmount, self.amount, stepType)
            self.ood[isdh_comp].append(step)

        elif stepAmount < 0:
            assert self.ood[isdh_comp][-1] == DeformationStep(-stepAmount,
                                                              self.amount,
                                                              stepType)
            step = self.ood[isdh_comp].pop()

        assert stepAmount != 0

    def update_amount(self, amount):
        self.amount += amount

    def init_ood(self):
        for isdh_comp in self.i_s:
            self.ood[isdh_comp] = [ ]

    def copy_ood(self):
        copy = dict()
        for key, value in self.ood.items():
            copy[key] = value.copy()
        return copy 

    def save_ood(self):        
        self.d_h.append(self.copy_ood())
        
