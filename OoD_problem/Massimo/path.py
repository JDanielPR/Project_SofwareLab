from itertools import permutations
import path_solution as ps
class Path:
    def __init__(self):
        self.component_list = [ ]
        self.solution_list = [ ]
#        self.solution_list = None

    def solve(self):
#        self.solution_list = list(permutations(self.component_list))
        for solution in permutations(self.component_list):
            self.solution_list.append(ps.PathSolution(solution))

    def restore(self):
        for component in self.component_list:
            component.restore()
            
##    def __repr__(self):
##        string = ""
##        for x in self.solution_list[:-1]:
##            string += str(x)
##            string += "\n"
##        string += str(self.solution_list[-1])
##        return string

    def sort_components(self):
        self.component_list.sort(key = lambda c : c.left_node.x_position)

    def compute_neighbours(self):
        pass


            
