class SolutionCollector:
    def __init__(self):
        self.current_amount_of_deformation = 0
        self.initial_state = [ ]
        self.deformation_history_list = [ ]

    def add_deformation_history(self):
        print('\nadd_deformation_history')
        self.current_amount_of_deformation = 0
        self.deformation_history_list.append(dict())

        for isdh_comp in self.initial_state:
            self.deformation_history_list[-1][isdh_comp] = [ ]

    def delete_deformation_history(self):
        print('\ndelete_deformation_history')
        forget_me = self.deformation_history_list.pop()

    def initialize_deformation_history_list(self):
        for component in self.initial_state:
            pass 

