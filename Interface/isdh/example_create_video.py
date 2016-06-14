def create_video(list_of_components, deformation_history, frames_per_mm = 1 ):
    for component in list_of_components:
        component.do_what_needs_to_be_done(deformation_history)
###############################################################################

class Component:
    def __init__(self):
        pass
    
def do_what_needs_to_be_done(self, deformation_history):
    for deformation_step in deformation_history[self]:
        self.perform(deformation_step)
