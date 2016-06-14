# - # - # - # - # - # - # - # - PSEUDO CODE - # - # - # - # - # - # - # -  #

# the following function contains the whole solution of task 3.
# it takes an object of type Solution as an input 
def create_video(my_solution, frames_per_mm):
    # plot the structure at t=0
    my_solution.plot_initial_state()

    # add lights, cameras, the wall and other rendering stuff
    pass # IMPLEMENT ME

    # set current frame as the first one
    current_frame = 0
    # capture first frame
    pass # IMPLEMENT ME

    # loop over deformation steps
    for defo_step in my_solution.deformation_history:

        # plot the changes after the current deformation step
        defo_step.perform()

        # compute current frame
        current_frame = defo_step.amount*frames_per_mm

        # capture current frame
        pass # IMPLEMENT ME

    # other things...
    pass # IMPLEMENT ME

