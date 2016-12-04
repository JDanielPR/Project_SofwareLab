import imp
import sys
import os
sys.path.append('C:\\FAPSA18\\JDPR\\TUM\\Second_Semester\\Sofware_Lab\\BMW\\Sw_lab_tool')
from Visualization import CreateVideo
from pkg.structure_core import Structure
from pkg import read_xml

def main():
    ''' Define main function
    -Run this program in Blender interface
    -Choose the path of the xml and the location where the video will be saved
    -Modify this file with the respective parameters to run in the correct
    path.
    -Above all modify the parameters v_o of "Create video" to fit the
    structure into the video
    - Before running go to Window and open Toggle System Console
    -Active camara ortho to visualize the structure
    '''
    # read input
    struct = read_xml('C:\\FAPSA18\\JDPR\\TUM\\Second_Semester\\Sofware_Lab\\BMW\\Sw_lab_tool\\xml\\2_2.xml')
    # Solve problem
    [i_s, d_h] = struct.task_one()
    # Create video
    myVideo = CreateVideo.CreateVideo(i_s, 
                                      d_h[0], 
                                      50, 
                                      1, 
                                      1,
                                      'C:\\FAPSA18\\JDPR\\TUM\\Second_Semester\\Sofware_Lab\\BMW\\Animation_files\\OoD_animation\\Video\\OoD.avi')
                                
main()









