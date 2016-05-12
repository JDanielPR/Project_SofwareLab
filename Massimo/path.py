from itertools import permutations

class Path:
    def __init__(self):
        self.component_list = [ ]
        self.solution_list = None

    def solve(self):
        self.solution_list = permutations(self.component_list)

    def print_solution(self):
        solution_string = ""
        for solution in self.solution_list:
            for comp in solution:
                solution_string += comp.name
                solution_string += " "
            solution_string += "\n"
        print(solution_string)

            
