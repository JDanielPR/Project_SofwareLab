class PathSolution:
    def __init__(self, components_list):
        # a list of components e.g.:
        # [e10, e12, e14, e13]
        self.order_of_deformation = components_list

    def __repr__(self):
        return str(self.order_of_deformation)
