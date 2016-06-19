from . import deformation_step as ds

class Component:
    def __init__(self, name, x1, x2, defo_length, lp_level):
        # initial state
        self.name = name
        self.x1 = x1
        self.x2 = x2
        self.defo_length = defo_length
        self.lp_level = lp_level

        #
        self.solution_collector = None

    def save_deformation_step(self,
                              amount,
                              transformation):
        "It saves a DeformationStep associated with the component itself, \
given only the amount and type of transformation, as long as a \
solution_collector is defined"
        
        # if a solution_collector isn't defined
        if not self.solution_collector:
            # raise an exception
            NoSolutionCollector = Exception(
                "Unable to find a solution collector")
            raise NoSolutionCollector
        
        # if a solution_collector is defined
        else:
            # get the initial_deformation_amount
            initial_deformation_amount = self.solution_collector.\
                                         current_amount_of_deformation
            
            # get the last DeformationHistory object
            deformation_history = self.solution_collector.\
                                  deformation_history_list[-1]

            # get the last DeformationStep of the component
            last_deformation_step = deformation_history[self][-1]
            # where deformation_history[self] is a list

            # check if either a new DeformationStep has to be created
            # or the previous one can be enhanced
            if last_deformation_step.transformation == transformation and\
               last_deformation_step.frame_end == initial_deformation_amount:
                # the previous DeformationStep can be enhanced, since the
                # transformation is the same and since the current deformation
                # step comes right after the previous one

                # enhance DeformationStep
                last_deformation_step.amount += amount
                last_deformation_step.frame_end += amount

            else:
                # a new deformation step has to be created
                    
                # create the DeformationStep
                deformation_step = ds.\
                                   DeformationStep(amount,
                                                   initial_deformation_amount,
                                                   transformation)
                
                deformation_history[self].append(deformation_step)


