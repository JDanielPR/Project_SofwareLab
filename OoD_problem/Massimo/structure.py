from itertools import product
from . import loadpath as lp
from . import connectionpath as cp
from . import structure_solution as ss
import isdh

class Structure:
    def __init__(self):
        self.path_list = [ ]
        self.solution_list = None
        self.deformation_history = [ ]
#        self.solution_list = [ ]

    def solve(self):
        # initialize a list of isdh.DeformationHistory objects
        self.deformation_history = [ ]

        # solve each path independently (just loadpaths)
        for path in self.path_list:
            if type(path) is lp.Loadpath:
                path.solve()
            
        # create a list containing the path solution_list of each path
            # to be more clear:
            # - a struct is made of paths
            # - a path is made of components
            #
            # THEREFORE
            #
            # - a path solution is a list of components
            #         e.g. [comp1, comp2, ...]
            # - a path solution_list is a list of path solutions
            #         e.g. [[comp1, comp2, ...], [...], ...]
            # - a struct solution is a list of path solution, so it looks like
            #   a path solution_list, but in this case each path solution
            #   belongs to a different path
            #         e.g. [[path1 solution], [path2 solution], ...]
            #           or [[other path1 solution], [other path2 solution], ...]
        list_of_path_solution_list = [path.solution_list for path
                                      in self.path_list
                                      if type(path) is lp.Loadpath]

        # save, as structure solution_list, the product set of each
        # path_solution_list
#        self.solution_list = list(product(*list_of_path_solution_list))

#        for solution in product(*list_of_path_solution_list):
#            self.solution_list.append(ss.StructureSolution(solution))

##        all_solutions = (ss.StructureSolution(solution, self) for solution
##                         in product(*list_of_path_solution_list))
##        for sol in all_solutions:
##            sol.test()
        all_solutions = (ss.StructureSolution(solution, self) for solution
                         in product(*list_of_path_solution_list))
        self.solution_list = (sol for sol in all_solutions
                              if sol.test())

##        self.solution_list = filter(ss.StructureSolution.test,
##                                    all_solutions)
        # test the given solutions
##        for solution in self.solution_list:
##            valid = test(solution) # implement this
##            if not valid:
##                self.solution_list.remove(solution)

    def restore(self):
        for path in self.path_list:
            path.restore()


    def print_solution(self):
        # ask the user
        while True:
            # print number of solutions
            user_input = input("Do you want to know the number of solutions, \
that have been found? y/n\
\n\n\t### it will take around 1 second every 1,000 solutions ###\n\n")
            if user_input == "y" or user_input == "Y":
                self.solution_list = list(self.solution_list)
                number_of_sol = len(self.solution_list)
                number_of_sol_string = '{:,}'.format(number_of_sol)
                print("Found %s solutions for the given structure."
                      % number_of_sol_string)
                break
            elif user_input == "n" or user_input == "N":
                break

        # ask the user
        while True:
            user_input = input("Do you want to see all of them? y/n\t")
            if user_input == "y" or user_input == "Y":        
                # loop over all the elements
                for i,x in enumerate(self.solution_list, 1):
                    string = ""
                    # add number of solution right justified
                    string += str(i).rjust(10) + ". "
                    # add solution
                    string += str(x)

                    print(string)
                break
            
            elif user_input == "n" or user_input == "N":
                break
        return ""               

    def print_read_data(self):
        for path in self.path_list:
            if type(path) is lp.Loadpath:
                if not path.component_list:
                    print("Loadpath", path.id, "is empty")
                else:
                    print("Loadpath", path.id, "has these components:")
                    for comp in path.component_list:
                        comp.print_current_info("\t")
            elif type(path) is cp.Connectionpath:
                print("Found a connectionpath with this component:")
                path.component_list[0].print_current_info("\t")
                
