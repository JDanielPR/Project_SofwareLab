from itertools import permutations

class Path:
    def __init__(self):
        self.component_list = [ ]
        self.solution_list = None

    def solve(self):
        self.solution_list = list(permutations(self.component_list))
        
    def __repr__(self):
        string = ""
        for x in self.solution_list[:-1]:
            string += str(x)
            string += "\n"
        string += str(self.solution_list[-1])
        return string

    def sort_components(self):
        self.component_list.sort(key = lambda c : c.left_node.x_position)

    


            

