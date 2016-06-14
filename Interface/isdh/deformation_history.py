class DeformationHistory:
    def __init__(self):
        self.deformation_history = { }
        # e.g. {
        #       Component1:[defo_step1, defo_step2, ...],
        #       Component2:[defo_step1, defo_step2, ...],
        #       Component3:[defo_step1, defo_step2, ...],
        #       ...
        #       }
        # where Component1, Component2, ... is a component and
        # [defo_step1, defo_step2, ...] is its deformation history solution
