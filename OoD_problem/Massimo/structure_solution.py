import connectionpath as cp

class StructureSolution:
    def __init__(self, path_solution_list, structure):
        # a list of path solutions e.g.:
        # [[e10, e12, e14, e13], [e23, e21, e22]]
        self.global_order_of_deformation = path_solution_list
        self.structure = structure

    def __repr__(self):
        return str(self.global_order_of_deformation)

    def test(self):
        string = ''.join('#' for i in range(79))
        print('\n\n',string,sep='')
        print('testing', self)
        # efficiency will come next...
        # now let's try to get a working function

        # restore undeformed struture
        self.structure.restore()
        
        while True:
##            self.structure.print_read_data()
            try:
                # create a list of the first components that are still
                # deformable
                components_to_deform = [
                    next(component for component
                         in path_solution.order_of_deformation
                         if component.current_deformable_length > 0)
                    for path_solution
                    in self.global_order_of_deformation]

##                print('i found this')
##                print(components_to_deform)

                min_deformable_length = min(component.current_deformable_length
                                            for component
                                            in components_to_deform)
##                print('the min defo lenght is', min_deformable_length)
            except StopIteration:
##                print("stop iteration")
                break

            # perform deformation step
            for component in components_to_deform:
                component.deform(min_deformable_length)

            # look for connections that became longer
            for path in self.structure.path_list:
                if type(path) is cp.Connectionpath:
                    for connection in path.component_list:
                        if connection.previous_deformable_length < \
                           connection.current_deformable_length:
                            # if at least one is found
##                            print(connection, 'became longer')
##                            print('returning False')
                            return False
                        else:
                            # else re-initialize the attribute
                            # previous_deformable_length
##                            print(connection, 'did NOT became longer')
                            connection.previous_deformable_length = \
                                connection.current_deformable_length
##        print('returning True')
        return True   
