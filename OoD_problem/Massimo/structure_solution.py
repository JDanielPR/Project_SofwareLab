from . import connectionpath as cp
from . import deformation_step as ds
# import isdh.deformation_history

class StructureSolution:
    def __init__(self, path_solution_list, structure):
        # a list of path solutions e.g.:
        # [[e10, e12, e14, e13], [e23, e21, e22]]
        self.global_order_of_deformation = path_solution_list
        self.deformation_step = ds.DeformationStep()
        self.structure = structure

    def __repr__(self):
        return str(self.global_order_of_deformation)

    def test(self):
        """Tests the validity of the structure solution: True or False."""
        
        # efficiency will come next...
        # now let's try to get a working function

        # restore undeformed struture
        self.structure.restore()

        # loop deformation step after deformation step, until either an invalid
        # deformation step is found or the last one was performed
        while True:
            
        # get the next deformation step as a list of components to deform
            components_to_deform = [ ]
            for path_solution in self.global_order_of_deformation:
                # try to get the next deformable component
                try:
                    member = next(x for x
                                  in path_solution.order_of_deformation
                                  if x.current_deformable_length > 0)
                except StopIteration:
                    # no more deformable components in this path:
                    # the solution is valid

                    # restore undeformed struture
                    self.structure.restore()
                    return True

                # a deformable component was found: append it
                components_to_deform.append(member)
            
        # get the deformation length of the next step and test the validity of
        # the next deformation step

##            print('components_to_deform:', components_to_deform)
            # re-initialize the information collector 
            self.deformation_step.re_init()

            # collect infos
            for component in components_to_deform:
                # indirectly calls all components involved in the deformation
                # step and saves the infos in the information collector
############################
##                component.print_current_info()
                component.virtual_deform(self.deformation_step)

            # test the deformation step
            # if not valid, discard the whole solution
            if not self.deformation_step.test():
                # the deformation step isn't valid
                
                # restore undeformed struture
                self.structure.restore()
                return False

            else:
                # the deformation step is valid and the information collector
                # self.deformation_step has collected all the infos:
                #   e.g. the amount of deformation is
                #        self.deformation_step.max_deformation

###############################################################################
                # WRONG ASSUMPTION, JUST TO AVOID INFINITE LOOPS
                # if the max_deformation allowed is 0 discard the deformation
                # step
                if self.deformation_step.max_deformation == 0:
                    
                    # restore undeformed struture
                    self.structure.restore()
                    return False                

            # if valid, perform it
                # the deformation step is valid
                
                # loop over the components to deform
                for component in components_to_deform:
                    # deform the component
##                    print('deforming',component,'of',self.deformation_step.max_deformation)
                    component.deform(self.deformation_step.max_deformation)
                
                # update the amount of deformation
##                print('update amount of deformation in solution_collector:')
##                print('\t',self.structure.solution_collector.current_amount_of_deformation, '-->',self.structure.solution_collector.current_amount_of_deformation + self.deformation_step.max_deformation)
                self.\
                       structure.\
                       solution_collector.\
                       current_amount_of_deformation += self.deformation_step.max_deformation 

def deformable_members_generator(path_solution):
    for component in path_solution:
        if component.current_deformable_length >0:
            yield component

###############################################################################
##  how to find components_to_deform?
##
##  components_to_deform is a list containing all the components that will
##  be deformed in the next deformation step.
##
##  solution 1:

####    path_sol_list = [deformable_members_generator(path_solution.
####                                                  order_of_deformation)
####                     for path_solution in self.global_order_of_deformation]
####
####    for components_to_deform in (zip(*path_sol_list)):            

##      this way the components to deform are called only once.      
##      e.g.:
##            
##      o---I----o-II--o-III-o            oo-II--o-III-o
##                                ----->
##      o------I-------o--II-o            o------o--II-o
##            
##      The first element of each loadpath is called.
##      Then the first element of the second loadpath should be called, since 
##      it's not completely deformed. Instead the second element of each
##      loadpath is called:
##            
##      oo-II--o-III-o            ooo-III-o
##                       ----->            
##      o------o--II-o            o------oo
##
##      Then the third element of each loadpath would be called, but the second 
##      loadpath doesn't have a third element, so nothing is called and the
##      structure remains undeformed.
##      This solution doesn't make sense!!!
##
##  solution 2:
            
####        while True:
####            components_to_deform = [ ]
####            for path_solution in self.global_order_of_deformation:
####                try:
####                    #get next deformable element
####                    print("Path solution:",path_solution)
####                    
####                    member = next(x for x
####                                  in path_solution.order_of_deformation
####                                  if x.current_deformable_length > 0)
####                except StopIteration:
####                    return True
####
####                components_to_deform.append(member)
####            
####            # test solution with components_to_deform found            

##      This way the first still deformable component is called.
##      In this case the solution of the previous example is as expected:
##
##      o---I----o-II--o-III-o          oo-II--o-III-o          ooo-III-o
##                              ----->                  ----->
##      o------I-------o--II-o          o------o--II-o          o-o--II-o
##
##                ooo-IIIo          oooo
##        ----->            ----->
##                oo--II-o          oo-o
##
##      But in this case:
##
##        o---I---o-II-o
##               /          <--- rigid connection
##        o-II--o---I--o
##
##      - the first two elements of each loadpath are called
##      - the maximum deformation allowed is computed, which is zero, since the
##          connection is rigid
##      - the two elements get deformed by a zero displacement of their right
##          node
##
##      for the next deformation step, the first two deformable elements of
##      each loadpath are the same as before: the program runs into an infinite
##      loop!!!
##
