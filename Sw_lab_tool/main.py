import imp
import sys
import os
sys.path.append('folder with files path')
from Visualization import CreateVideo
from pkg.structure_core import structure
from pkg.read_xml import read_xml

def main():
    ''' Define main function
    -Run this program in Blender interface
    -Choose the path of the xml and the location where the video will be saved(use //)
    -Modify this file with the respective parameters to run in the correct
    path.
    -Above all modify the parameters v_o of "Create video" to fit the
    structure into the video
    - Before running go to Window and open Toggle System Console
    -Active camera ortho to visualize the structure
    '''
    # Read input
    struct = read_xml('xml_path')
    # Solve problem
    [i_s, d_h] = struct.task_one()
    # Create video
    myVideo = CreateVideo.CreateVideo(i_s, 
                                      d_h[0], 
                                      50, 
                                      1, 
                                      1,
                                      'video_path')
                                
main()









