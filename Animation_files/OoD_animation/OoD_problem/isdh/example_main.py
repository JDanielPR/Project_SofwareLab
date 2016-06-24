# import modules
import solver_module as s
import animation_module as a

## * * * * * . . . . . * * * * * . . . . . * * * * * . . . . . * * * * *
##                           REMARK
## the solver_module has to implement:
## - a function called read_xml() that takes an .xml file as input and
##   outputs an object of a class
## - a method of that class called solve() that doesn't take anything as
##   input and outputs the 2 lists of isdh objects defined below
##
## * * * * * . . . . . * * * * * . . . . . * * * * * . . . . . * * * * *
   
# create an object of a class defined in the solver module
# and store everything inside of it
structure = s.read_xml('some_folder/my_xml_file.xml')

##############################################################################
# solve the structure
[initial_state, deformation_history] = structure.solve()
# where:
# initial_state = [isdh.Component, isdh.Component, ...]
# deformation_history = [isdh.DeformationHistory, isdh.DeformationHistory, ...]

## * * * * * . . . . . * * * * * . . . . . * * * * * . . . . . * * * * *
##                           REMARK
## the isdh module works as an interface between the solver_module and
## the animation_module.
## No matter how structure.solve() works: the output is defined so that
## it can be used as an input for a.create_video()
##
## * * * * * . . . . . * * * * * . . . . . * * * * * . . . . . * * * * *

##############################################################################
# create the video
n = 0 # which solution should be used to create the video?
a.create_video(initial_state, deformation_history[n], frames_per_mm = 1)

## * * * * * . . . . . * * * * * . . . . . * * * * * . . . . . * * * * *
##                           REMARK
## the animation_module has to implement a function called create_video()
## that takes as input three arguments of type:
##  - [isdh.Component, isdh.Component, ...]
##  - isdh.DeformationHistory
##  - integer
##
## * * * * * . . . . . * * * * * . . . . . * * * * * . . . . . * * * * *
