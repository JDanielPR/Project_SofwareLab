from itertools import permutations

class Path:
    def __init__(self):
        self.component_list = [ ]
        self.solution_list = None

    def solve(self):
        self.solution_list = list(permutations(self.component_list))

    def solution_string(self, index):
        """returns a string of the solution in path.solution_list[index].
The string is structured so (comp.name, comp.name, ...)"""
        solution_string = "("
        last = len(self.solution_list[index]) - 1
        for i,component in enumerate(self.solution_list[index]):
            solution_string += component.name
            if i != last:
                solution_string += ", "
        return solution_string + ")"

    def path_solution_string(self):
        """returns a string with the list of all the solutions.
The string is structured so:
(comp1.name, comp2.name, comp3.name)
(comp1.name, comp3.name, comp2.name)
(comp2.name, comp1.name, comp3.name)
                ...
(..., ..., ...)."""
        path_solution_string = ""
        last = len(self.solution_list) - 1
        for i, solution in enumerate(self.solution_list):
            path_solution_string += self.solution_string(i)
            if i != last:
                path_solution_string += "\n"
        return path_solution_string

            

