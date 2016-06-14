class Component:
    def __init__(self, name, x1, x2, defo_length, lp_level):
##        # dictionary with DeformationStep:operation_type
##        self.operation = { }
##        # e.g. {step1:'d', step4:'m', step5:'d', step6:'b', step7:'m'}
##        # LEGEND:
##        # 'd': the element deforms
##        # 'm': the element moves
##        # 'b': the element breaks
##        # REMARK:
##        # breakable connections have to be modelled as 2 components! This way
##        # they can move independently once broken with no complications


        #####################
        self.name = name
        self.x1 = x1
        self.x2 = x2
        self.defo_length = defo_length
        self.lp_level = lp_level
        self.deformation_history = [ ] 

##    def update_state(defo_step, amount):
##        operation = self.operation[defo_step]
##
##        if operation == 'd':
##            self.deform(amount)
##        elif operation == 'm':
##            self.move(amount)
##        elif operation == 'b':
##            self.break_me()

    def deform(self, amount):
        """TO BE IMPLEMENTED
It deforms the rectangle."""
        pass

    def move(self, amount):
        """TO BE IMPLEMENTED
It moves the rectangle"""
        pass

    def break_me(self):
        """TO BE IMPLEMENTED
It breaks the connection, perhaps changing its colour?"""
        pass

    def display(self):
        """TO BE IMPLEMENTED
It displays the component actual state."""

def perform(self, defo_step):
    if defo_step.transformation == 'm':
        #move
        self.move(defo_step.amount,
                  defo_step.frame_begin,
                  defo_step.frame_end)
        
    elif defo_step.transformation = 'd':
        #deform
        self.deform(defo_step.amount,
                    defo_step.frame_begin,
                    defo_step.frame_end)

class DeformationStep:
    def __init__(self):
        self.amount =
        self.frame_begin = 
        self.frame_end =
        self.transformation = # 'm' or 'd'
