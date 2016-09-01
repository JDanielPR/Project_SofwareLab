import imp
import initialization
import Structure
import sys
sys.path.append('C:\\FAPSA18\\JDPR\\TUM\\Second_Semester\\Sofware_Lab\\BMW\\Animation_files\\OoD_animation')
import OoD_problem

# Load libraries
imp.reload(initialization)   
imp.reload(Structure)
imp.reload(OoD_problem)
imp.reload(sys)

# Define main function
def main():

    initialization.initialize()  #Clean all and positionate the cursor
    
    struct = OoD_problem.Massimo.read_xml() 
    [i_s,d_h] = struct.solve()   #i_s (initial status) / d_h (deformation history)
    myStructure = Structure.Structure(i_s , d_h[1])
    
main()








