class DeformationStep:
    def __init__(self, amount):
        # list of deformed / moved components
        self.active_components = [ ]

        # length, amount, pseudo-time...
        self.amount = amount

    def perform(self):
        for comp in self.active_components:
            comp.update_state(self, amount)

