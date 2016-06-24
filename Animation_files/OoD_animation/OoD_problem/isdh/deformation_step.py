class DeformationStep:
    def __init__(self, amount, initial_deformation_amount, transformation):
        self.amount = amount
        self.frame_begin = initial_deformation_amount
        self.frame_end = initial_deformation_amount + amount
        self.transformation = transformation # 'm' or 'd'
##        # LEGEND:
##        # 'd': the element deforms
##        # 'm': the element moves
##        # 'b': the element breaks

    def __repr__(self):
        return self.transformation + ': ' + str(self.amount)
