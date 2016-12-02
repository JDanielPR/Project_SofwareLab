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
        """Return the string representation of the object.
        
        Args:
            nothing is taken
        Returns:
            string
        Raises:
            nothing is raised
        """
        return self.transformation + ': ' + str(self.amount)

    def __eq__(self, other):
        """Return self == other.
        
        Args:
            other:
                DeformationStep object.
        Returns:
            True or False.
        Raises:
            NotImplementedError is raised, if other is not a DeformationStep
            object.
        """
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        raise NotImplementedError

    def __ne__(self, other):
        """Return self != other.
        
        Args:
            other:
                DeformationStep object.
        Returns:
            True or False.
        Raises:
            NotImplementedError is raised, if other is not a DeformationStep
            object.
        """

        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        raise NotImplementedError

    def print(self):
        """Print a detailed description of the object.

        Args:
            nothing is taken.
        Returns:
            nothing is returned.
        Raises:
            nothing is raised.
        """
        if self.transformation == 'd':
            transformation = "deform"
        if self.transformation == 'm':
            transformation = "move"
        print("from {0} to {1}: {2} by {3}"
              .format(self.frame_begin,
                      self.frame_end,
                      transformation,
                      self.amount)
              )
