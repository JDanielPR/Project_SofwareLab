from itertools import product

class Structure:
    def __init__(self):
        self.path_list = [ ]
        self.solution_list = None

    def solve(self):
        # solve each path independently
        for path in self.path_list:
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
        list_of_path_solution_list = [x.solution_list for x in self.path_list]

        # save, as structure solution_list, the product set of each
        # path_solution_list
        self.solution_list = list(product(*list_of_path_solution_list))

    def __repr__(self):
        
        # loop over all the elements
        for i,x in enumerate(self.solution_list, 1):
            string = ""
            # add number of solution right justified
            string += str(i).rjust(10) + ". "
            # add solution
            string += str(x)

            print(string)
        
        return string
               
