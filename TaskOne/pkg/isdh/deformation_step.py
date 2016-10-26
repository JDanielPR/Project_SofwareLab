class DeformationStep:
    def __init__(self, amount, initial_deformation_amount, transformation):
        self.amount = amount
        self.frame_begin = initial_deformation_amount
        self.frame_end = initial_deformation_amount + amount
        self.transformation = transformation # 'm' or 'd' or 'b'
##        # LEGEND:
##        # 'd': the element deforms
##        # 'm': the element moves
##        # 'b': the element breaks

    def __repr__(self):
        return self.transformation + ': ' + str(self.amount)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def print(self):
        for key, item in self.__dict__.items():
            print(key, ': ', item)
