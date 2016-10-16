import imp
import CreateVideo
import sys
sys.path.append('C:\\FAPSA18\\JDPR\\TUM\\Second_Semester\\Sofware_Lab\\BMW\\Animation_files\\OoD_animation')
import OoD_problem
import fakeSolver

# Load libraries
imp.reload(CreateVideo)
imp.reload(OoD_problem)
imp.reload(sys)
imp.reload(fakeSolver)

# Define main function
def main():
    #struct = OoD_problem.Massimo.read_xml() # Read xml
    #[i_s,d_h] = struct.solve()              # Solve problem of OoD : i_s (initial status) / d_h (deformation history)
    #myVideo = CreateVideo.CreateVideo(i_s , d_h[3],1, 'C:\\FAPSA18\\JDPR\\TUM\\Second_Semester\\Sofware_Lab\\BMW\\Animation_files\\OoD.avi')
    [i_s,d_h] = fakeSolver.fake_solver()
    #i_s (initial status) / d_h (deformation history) / frame per second / location of the video
    myVideo = CreateVideo.CreateVideo(i_s, 
                                      d_h[1], 
                                      30, 
                                      1, 
                                      'C:\\FAPSA18\\JDPR\\TUM\\Second_Semester\\Sofware_Lab\\BMW\\Animation_files\\OoD.avi')
    
main()








