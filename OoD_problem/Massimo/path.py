from itertools import permutations

class Path:
    def __init__(self):
        self.component_list = [ ]
        self.solution_list = None

    def solve(self):
        self.solution_list = list(permutations(self.component_list))

    def print_solution(self, index):
        solution_string = "("
        last = len(self.solution_list[index]) - 1
        for i,component in enumerate(self.solution_list[index]):
            solution_string += component.name
            if i != last:
                solution_string += ", "
        solution_string += ")"
        print(solution_string)

    def print_solution_list(self):
        solution_string = ""
        for solution in self.solution_list:
            for comp in solution:
                solution_string += comp.name
                solution_string += " "
            solution_string += "\n"
        print(solution_string)

            

