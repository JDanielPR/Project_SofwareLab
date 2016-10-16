import deformation_step as ds

class Component:
    def __init__(self, name, x1, x2, defo_length, lp_level1, lp_level2, p=0):
        # initial state
        self.name = name
        self.x1 = x1
        self.x2 = x2
        self.defo_length = defo_length
        self.lp_level1 = lp_level1
        self.lp_level2 = lp_level2
        # mass part
        if p:
            self.mass = True # True or False
            self.mass_position = p # [345, 355, ...] for example (absolute position)
