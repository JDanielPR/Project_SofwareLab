from itertools import product
from . import loadpath as lp
from . import connectionpath as cp
from . import structure_solution as ss
from ..isdh import solution_collector as sc

class Structure:
    def __init__(self):
        self.path_list = [ ]
        self.solution_list = [ ]
        self.solution_collector = sc.SolutionCollector()

    def solve(self):
        # solve each path independently (just loadpaths)
        for path in self.path_list:
            if type(path) is lp.Loadpath:
                path.solve()
            
        # create a list containing the path solution_list of each path
            # to be more clear:
            # - a structure is made of paths
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
            #         e.g. Given the path solution_list:
            #              path1    [[solution1], [solution2], ... ]
            #              path2    [[solution1], [solution2], ... ]
            #              ...
            #              path_n   [[solution1], [solution2], ... ]
            #
            #              a structure solution appears as following:
            #              [[path1 solution], [path2 solution], ...]
            #           or [[other path1 solution], [other path2 solution], ...]
            #
            # FINALLY
            #
            # - a list containg the path solution_list of each path appears as:
            #       [[[solution1], [solution2], ... ],  <-- path1
            #        [[solution1], [solution2], ... ],  <-- path2
            #        ...,
            #        [[solution1], [solution2], ... ]]  <-- path_n
        list_of_path_solution_list = [path.solution_list for path
                                      in self.path_list
                                      if type(path) is lp.Loadpath]

        # create a list with all the possible structure solutions
            # given list_of_path_solution_list, it just takes to compute the
            # product set of all its members.
            # i.e. take one solution out of each path solution_list
        all_solutions = (ss.StructureSolution(solution, self) for solution
                         in product(*list_of_path_solution_list))
        
        # check for each solution in all_solutions wheter it makes sense or not
        for solution in all_solutions:
            
            # create space for saving a new solution in the solution collector
            self.solution_collector.add_deformation_history()

            print('testing', solution)
            if solution.test():
                # if the solution is valid, save it (implicitly done in the
                # test() function)

                # save the solution in the old format in solution_list
                self.solution_list.append(solution)
            
            else:
                # if the solution is not valid, discard it
                self.solution_collector.delete_deformation_history()

        # return the initial_state and the deformation_history_list
        return [self.solution_collector.initial_state,
                self.solution_collector.deformation_history_list]

    def restore(self):
        """It restores the undeformed configuration of the structure."""
        for path in self.path_list:
            path.restore()

    def register_components(self):
        """It assign the solution_collector of the structure to all its \
isdh_component and it initialize the solution_collector.initial_state."""
        print('Structure.register_components() has been called')
        # loop over components
        for path in self.path_list:
            for component in path.component_list:
                print('register', component)
                # assign the solution_collector to each of them
                component.\
                            isdh_component.\
                            solution_collector = self.solution_collector

                # append the isdh_component to the initial_state
                self.solution_collector.initial_state.append(component.
                                                             isdh_component)


    def ask_for_print_solution(self):
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
    def print_solution(self):
        # loop over all the elements
        for i,x in enumerate(self.solution_list):
            string = ""
            # add number of solution right justified
            string += str(i).rjust(10) + ". "
            # add solution
            string += str(x)

            print(string)    

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
                
