class SolutionCollector:
    def __init__(self):
        self.current_amount_of_deformation = 0
        self.initial_state = [ ]
        self.deformation_history_list = [ ]

    def add_deformation_history(self):
        self.current_amount_of_deformation = 0
        self.deformation_history_list.append(dict())

    def delete_deformation_history(self):
        forget_me = self.deformation_history_list.pop()

    def initialize_deformation_history_list(self):
        for component in self.initial_state:
            pass 

