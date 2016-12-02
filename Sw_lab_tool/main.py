import imp
import sys
import os
sys.path.append('path of the folder where the main is')
from Visualization import CreateVideo
from pkg.structure_core.structure import Structure
from pkg.read_xml import read_xml

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
    struct = read_xml('path of the xml')
    # Solve problem
    [i_s, d_h] = struct.task_one()
    # Create video
    myVideo = CreateVideo.CreateVideo(i_s, 
                                      d_h[0], 
                                      50, 
                                      1, 
                                      1,
                                      'path where the video will be created')
                                
main()









