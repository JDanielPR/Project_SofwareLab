import imp
import sys
sys.path.append('C:\\FAPSA18\\JDPR\\TUM\\Second_Semester\\Sofware_Lab\\BMW\\Animation_files\\OoD_animation')
from Visualization import CreateVideo
import pkg
import pkg.tree_core
from pkg.structure_core.Structure import Structure
from pkg.read_xml2 import read_xml
import pkg.GapsHandeling


imp.reload(sys)
imp.reload(pkg)
# Define main function
def main():
    # read input
    struct = read_xml('C:\\FAPSA18\\JDPR\\TUM\\Second_Semester\\Sofware_Lab\\BMW\\Animation_files\\OoD_animation\\xml\\2_2.xml')
    # Solve problem
    [i_s, d_h] = struct.task_one()
    # Create video
    myVideo = CreateVideo.CreateVideo(i_s, 
                                      d_h[0], 
                                      50, 
                                      1, 
                                      3,
                                      'C:\\FAPSA18\\JDPR\\TUM\\Second_Semester\\Sofware_Lab\\BMW\\Animation_files\\OoD_animation\\Video\\OoD.avi')
                                      
main()








